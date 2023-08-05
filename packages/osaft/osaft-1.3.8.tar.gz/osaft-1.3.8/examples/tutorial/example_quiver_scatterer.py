"""
Scatterer: Acoustic velocity plots with arrows
==============================================

This example shows how to plot the acoustic velocity and also add arrows within
the plot showcasing the magnitude and direction of the acoustic fluid velocity.

This example is very similiar to :ref:`the example of quiver plots in a fluid
<sphx_glr_examples_tutorial_example_quiver_fluid.py>`. Therefore, we will keep
the text very short here. If you want to have more explanations, check out the
linked example.
"""

# %%
from matplotlib import pyplot as plt

import osaft

# --------
# Geometry
# --------
# Radius
R_0 = 30e-6  # [m]

# ---------------------------
# Properties of the Scatterer
# ---------------------------
# Speed of sound
c_sc = 350  # [m/s]
# Density
rho_sc = 1_020  # [kg/m^3]

# ---------------------------
# Properties of Water
# ---------------------------
# Speed of sound
c_water = 1_500  # [m/s]
# Density
rho_water = 997  # [kg/m^3]

# --------------------------------
# Properties of the Acoustic Field
# --------------------------------
# Frequency
f = 1e7  # [Hz]
# Pressure
p_0 = 1e5  # [Pa]
# Wave type
wave_type = osaft.WaveType.TRAVELLING
# Position of the particle in the field
position = osaft.pi / 4  # [rad]

# ----------------
# Truncation Limit
# ----------------
# Number of scattering modes that are considered
N_max = 5

# %%
# Initialization of the ``ScatteringField`` class of the ``yosioka1955``
# solution

sol = osaft.yosioka1955.ScatteringField(
    f=f,
    R_0=R_0,
    rho_s=rho_sc,
    c_s=c_sc,
    rho_f=rho_water,
    c_f=c_water,
    p_0=p_0,
    wave_type=wave_type,
    position=position,
    N_max=N_max,
)

# %%
# Initialization of plotter object

plotter = osaft.ParticleScatteringPlot(sol, cmap="plasma")

# %%
# Acoustic velocity and quiver arrows

fig, ax = plotter.plot_velocity(
    symmetric=True,
    inst=True,
    quiver_color="white",
)
ax.set_title("Acoustic Velocity Magnitude + Quiver")
fig.tight_layout()
plt.show()

# %%
# Evolution plot

fig, _ = plotter.plot_velocity_evolution(
    quiver_color="white",
    tripcolor=True,
    figsize=(12, 12),
)
plt.show()

# %%
# Animated velocity arrows for second mode only

anim = plotter.animate_velocity(quiver_color="white", mode=2)
anim.resume()
plt.show()

# %%
# Animated velocity arrows for all modes

anim = plotter.animate_velocity(quiver_color="white")
anim.resume()
plt.show()
