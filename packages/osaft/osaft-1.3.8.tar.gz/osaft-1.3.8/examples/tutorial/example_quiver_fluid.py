"""
Fluid: Acoustic velocity plots with arrows
==========================================

This example shows how to plot the acoustic velocity and also add arrows within
In this example we illustrate how we can use arrow plots to illustrate both
magnitude and direction of the acoustic particle velocity.
"""

# %%
# In this example we study a glass sphere in a viscous fluid.

from matplotlib import pyplot as plt

import osaft

# --------
# Geometry
# --------
# Radius
R_0 = 50e-6  # [m]

# -------------------
# Properties of Glass
# -------------------
# Speed of sound
c_1_glass = 4_521  # [m/s]
c_2_glass = 2_226  # [m/s]
# Density
rho_glass = 2_240  # [kg/m^3]

# ---------------------------
# Properties of Viscous Fluid
# ---------------------------
# Speed of sound
c_oil = 1_400  # [m/s]
# Density
rho_oil = 900  # [kg/m^3]
# Viscosity
eta_oil = 0.04  # [Pa s]
zeta_oil = 0  # [Pa s]

# --------------------------------
# Properties of the Acoustic Field
# --------------------------------
# Frequency
f = 10e5  # [Hz]
# Pressure
p_0 = 1e5  # [Pa]
# Wave type
wave_type = osaft.WaveType.STANDING
# Position of the particle in the field
position = osaft.pi / 4  # [rad]

# %%
# Here, we are given the primary and the secondary wave speed of
# glass only. The model ``doinikov2021viscous``, however, takes the Young's
# modulus and the Poisson's ratio as input parameters. We therefore have to
# convert the properties. The ``ElasticSolid`` class offers such conversion
# methods.

E_s = osaft.ElasticSolid.E_from_wave_speed(c_1_glass, c_2_glass, rho_glass)
nu_s = osaft.ElasticSolid.nu_from_wave_speed(c_1_glass, c_2_glass)

sol = osaft.doinikov2021viscous.ScatteringField(
    f=f,
    R_0=R_0,
    rho_s=rho_glass,
    E_s=E_s,
    nu_s=nu_s,
    rho_f=rho_oil,
    c_f=c_oil,
    eta_f=eta_oil,
    zeta_f=zeta_oil,
    p_0=p_0,
    wave_type=wave_type,
    position=position,
)

# %%
# The next step is to initialise the plotter for the fluid.
# The option ``n_quiver_points`` let's use decide how many arrows along the
# z-direction and x-direction shall be plotted. If you chose the plotting
# option ``symmetric=False`` then the arrows along the x-direction will be
# halved.
# It is set in the constructor of the plotter, because the solution for the
# quiver arrows is stored within the class and it depends on the number of
# points. A change of this parameter will invoke new computation of the quiver
# directions. Per default it is set to ``n_quiver_points=21``. It is advisable
# to use an odd number if you like to change the parameter because this ensures
# that have a point at z=0, x=0.

plotter = osaft.FluidScatteringPlot(sol, r_max=3 * sol.R_0, cmap="Oranges")

# %%
# Let's start by simply plotting the acoustic velocity for ``phase=0``. In
# order to also show the arrows within the plot we need to add the option
# ``quiver_color='____'``. Per default ``quiver_color = None`` such that no
# arrows will be overlayed.

fig, ax = plotter.plot_velocity(quiver_color="black", symmetric=False)
ax.set_title("Acoustic Velocity Magnitude + Quiver")
fig.tight_layout()
plt.show()

# %%
# We can also have a look at first four modes and look how the velocity
# behaves for each of them individually.
# We start by creating a ``plt.subplots(...)`` with two rows and two columns.
#
fig, Axes = plt.subplots(2, 2, figsize=(12, 10))

# Now we loop over each of the ``plt.Axes`` within the ``Axes`` array and
# depict a different mode.

for i, ax in enumerate(Axes.flatten()):
    plotter.plot_velocity(mode=i, ax=ax, quiver_color="black")
    ax.set_title(f"Mode #{i}")

fig.tight_layout()
plt.show()

# %%
# The ``quiver_color=...`` option is also available for the
# ``plotter.plot_velocity_evolution(quiver_color=...)``. Let's check first if
# the incident acoustic field is depicted right. Therefore, we set
# ``incident=True`` and ``scattered=False``.


plotter.plot_velocity_evolution(
    quiver_color="black",
    mode=None,
    incident=True,
    scattered=False,
    symmetric=False,
    layout=(3, 3),
    figsize=(12, 12),
)
plt.show()

# %%
# And also for ``plotter.animate_velocity(quiver_color=...)``.

anim = plotter.animate_velocity(
    frames=100,
    interval=50,
    quiver=True,
    quiver_color="black",
    mode=None,
    incident=False,
    scattered=True,
)
plt.show()
