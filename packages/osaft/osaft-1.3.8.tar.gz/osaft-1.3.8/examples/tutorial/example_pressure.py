"""
Pressure Plot
=============

This examples shows you how to plot the pressure field.
"""

# %%
# As always we start off by importing the necessary Python modules. For our
# example we are going to need the osaft library, and the third party package
# Matplotlib.

from matplotlib import pyplot as plt

import osaft

# %%
# The next step is to define the properties for our example,
# these include the material properties, the properties of the acoustic field
# and the radius. We always assume SI-units.
#
# The wave type is set using the ``osaft.WaveType`` enum. Currently, there are
# two options:
# ``osaft.WaveType.STANDING`` and ``osaft.WaveType.TRAVELLING`` for a plane
# standing wave and a plane travelling wave, respectively.


# --------
# Geometry
# --------
# Radius
R_0 = 5e-6  # [m]

# -----------------
# Properties of copper
# -----------------
# Density
rho_cu = 8960  # [kg/m^3]
# Young's modulus
E_cu = 130e9  # [Pa]
# Possion ratio
nu_cu = 0.34  # [-]

# -------------------
# Properties of Water
# -------------------
# Speed of sound
c_w = 1_498  # [m/s]
# Density
rho_w = 997  # [kg/m^3]

# --------------------------------
# Properties of the Acoustic Field
# --------------------------------
# Frequency
f = 5e5  # [Hz]
# Pressure
p_0 = 1e5  # [Pa]
# Wave type
wave_type = osaft.WaveType.STANDING
# Position of the particle in the field
position = osaft.pi / 4  # [rad]

# %%
# Once all properties are defined we can initialize the solution instances for
# the scattering field. In this case we are using the model Hasegawa (1969).
# However, you can also chose any other model that has the scattering
# implemented.

sol = osaft.hasegawa1969.ScatteringField(
    f=f,
    R_0=R_0,
    rho_s=rho_cu,
    E_s=E_cu,
    nu_s=nu_cu,
    rho_f=rho_w,
    c_f=c_w,
    p_0=p_0,
    wave_type=wave_type,
    position=position,
)

# %%
# The next step is to initialise the plotter
plotter = osaft.FluidScatteringPlot(sol, r_max=5 * sol.R_0)


# %%
# In the first step we want to check if the set input pressure of ``p_0=1e5``
# matches with the calculated incident pressure field. Since we are in a
# standing wave field and will look at the time zero. We set the position to a
# multiple of ``osaft.pi`` such that we are the pressure maximum or minimum

sol.position = 0

fig, _ = plotter.plot_pressure(
    inst=True,
    tripcolor=False,
    incident=True,
    scattered=False,
)
fig.tight_layout()
plt.show()

# %%
# Alternatively, we can also look in an evolution plot how the pressure field
# evolves for different phase values. The default layout is 3x3 and can be
# adjusted with the option ``layout=(n_row, n_cols)``. Additionally we increase
# the figure size with ``figsize=(...)`` to enlarge the plots.

# sphinx_gallery_thumbnail_number = 2

plotter.plot_pressure_evolution(
    inst=True,
    tripcolor=False,
    layout=(5, 5),
    figsize=(10, 8),
    incident=True,
    scattered=False,
)
plt.show()

# %%
# Now lets see what the magnitude of the scattered field is

plotter.plot_pressure_evolution(
    inst=True,
    tripcolor=False,
    layout=(5, 5),
    figsize=(10, 8),
    incident=False,
    scattered=True,
)
plt.show()

# %%
# We might be also wondering how it looks for a travelling wave. Additionally,
# we can change the colormap. Note here, that we set the attribute
# ``plotter.div_cmap`` since the data that will be plotted will contain
# positive and negative values. Also, it is useful to have a diverging colormap
# that is NOT white in the center because the scatterer is depicted white in
# our plots.

sol.wave_type = osaft.WaveType.TRAVELLING
plotter.div_cmap = "RdYlBu"

plotter.plot_pressure_evolution(
    inst=True,
    tripcolor=False,
    layout=(5, 5),
    figsize=(10, 8),
    incident=False,
    scattered=True,
)
plt.show()

# %%
# Lastly we want to animate the pressure. Keep in mind that now the wave type
# is travelling

anim = plotter.animate_pressure(scattered=True, incident=False)
anim.resume()
plt.show()
