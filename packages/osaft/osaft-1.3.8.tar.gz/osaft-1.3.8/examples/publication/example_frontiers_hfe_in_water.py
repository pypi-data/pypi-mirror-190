"""
Frontiers: HFE Droplet in Water
===============================

This example corresponds to section 3.2 in
:ref:`our publication <CitingOsaft>`.
In this example we compute the acoustic radiation force (ARF) on a HFE droplet
suspended in water subjected to a plane standing wave. We compare
the theories from King (1934), Yosioka & Kawasima (1955), and Gor'kov (1962).
"""

# %%
# As always we start off by importing the nececassry Python modules. For this
# example we are going to need the osaft library, and the third party packages
# NumPy and Matplotlib.


import numpy as np
from matplotlib import pyplot as plt

import osaft

# %%
# The next step is to define the properties for our example,
# these include the material properties, the properties of the acoustic field
# and the radius of the particle. In the osaft library we are always
# assuming SI-units..
#
# The wave type is set using the ``osaft.WaveType`` enum. Currently, there are
# two options:
# ``osaft.WaveType.STANDING`` and ``osaft.WaveType.TRAVELLING`` for a plane
# standing wave and a plane travelling wave, respectively.


# --------
# Geometry
# --------
# Radius
R_0 = 1e-6  # [m]

# -----------------
# Properties of HFE
# -----------------
# Speed of sound
c_hfe = 659  # [m/s]
# Density
rho_hfe = 1_621  # [kg/m^3]

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
f = 5e6  # [Hz]
# Pressure
p_0 = 1e5  # [Pa]
# Wave type
wave_type = osaft.WaveType.STANDING
# Position of the particle in the field
position = np.pi / 4  # [rad]

# %%
# Once all properties are defined we can initialize the solution classes.
# In this example, we use the classes ``osaft.king1934.ARF()``,
# ``osaft.yosioka1955.ARF()``, and ``osaft.gorkov1962.ARF()``.


# Theory of King
king = osaft.king1934.ARF(
    f=f,
    R_0=R_0,
    rho_s=rho_hfe,
    rho_f=rho_w,
    c_f=c_w,
    p_0=p_0,
    wave_type=wave_type,
    position=position,
)

# Theory of Yosioka
yosioka = osaft.yosioka1955.ARF(
    f=f,
    R_0=R_0,
    rho_s=rho_hfe,
    c_s=c_hfe,
    rho_f=rho_w,
    c_f=c_w,
    p_0=p_0,
    wave_type=wave_type,
    position=position,
)

# Theory of Gor'kov
gorkov = osaft.gorkov1962.ARF(
    f=f,
    R_0=R_0,
    rho_s=rho_hfe,
    c_s=c_hfe,
    rho_f=rho_w,
    c_f=c_w,
    p_0=p_0,
    wave_type=wave_type,
    position=position,
)


# %%
# First, want to evaluate the compressibility of the droplet and the
# fluid and the scattering coefficients :math:`f_1` and :math:`f_2`.
# All these quantities are properties of the solution classes and can easily be
# evaluated.


# Compressibility
print(f"{yosioka.scatterer.kappa_f = :.2e}")
print(f"{yosioka.fluid.kappa_f = :.2e}")

# Gor'kov scattering coefficients
print(f"{gorkov.f_1 = :.2f}")
print(f"{gorkov.f_2 = :.2f}")


# %%
# Next, we want to compare the ARF from the different
# theories in the small particle limit. To plot the ARF
# we need to initialize an ``osaft.ARFPlot()`` instance.
# With the method ``add_solutions()`` we can add our models to the instance.
# With ``set_abscissa()`` we define the attribute that we want to
# plot the ARF against.  Here we select the radius `R_0`.
# Finally, ``osaft.ARFPlot.plot_solutions()`` will generate the plot.
# ``plot_solutions()`` returns two Matplotlib objects, a ``Figure`` and
# an ``Axes`` object. These can be used to further manipulate the plot and to
# save it.
# To display the plot we need to call ``plt.show()``

arf_plot = osaft.ARFPlot()

# Add solutions to be plotted
arf_plot.add_solutions(gorkov, yosioka, king)

# Define independent plotting variable (in this case the radius)
arf_plot.set_abscissa(np.linspace(1e-6, 15e-6, 300), "R_0")
fig, ax = arf_plot.plot_solutions()

# Setting the axis labels and the title
ax.set_xlabel(r"$R \, \mathrm{[m]}$")
ax.set_title(r"$\mathrm{(a)} \quad R \ll  \lambda$")

plt.show()

# %%
# .. note::
#       It is only possible to plot the ARF  against
#       properties that wrap an underlying ``PassiveVariable``, i.e. an input
#       parameter of the model.
#       You can get a list of all input variables using the method
#       ``input_variables()``.

print(f"{gorkov.input_variables() = }")
print(f"{yosioka.input_variables() = }")
print(f"{king.input_variables() = }")

# %%
# We redo our ARF plot, but this time the particle size is ranging from
# ``1e-6`` to ``120e-6`` meters.

# Plot
arf_plot.set_abscissa(np.linspace(1e-6, 120e-6, 300), "R_0")
fig, ax = arf_plot.plot_solutions()

# Additional Matplotlib commands for the publication
ax.set_xlabel(r"$R \, \mathrm{[m]}$")
ax.set_title(r"$\mathrm{(b)} \quad R \sim  \lambda$")
plt.show()


# %%
# Lastly, we want to plot the mode shapes of the particle. We can do this
# using the ``osaft.ParticleWireframePlot()`` class. To plot a specific model
# we have to pass this model when initializing ``ParticleWireframePlot``. We
# can also pass a value for the ``scale_factor``. The displacements in the
# mode shape plot are exaggerated, the ``scale_factor`` is the ratio between
# the maximal displacement and the particle radius in the exaggerated plot.
#
# In our example we plot the mode shape for three different radii. Again,
# we call ``plt.show()`` to display the plot.


# Creating a figure with subplots
fig, axes = plt.subplots(
    1,
    3,
    figsize=(9, 2.5),
    gridspec_kw={
        "width_ratios": [1, 1, 1],
    },
)

# List of radii
radii = [1e-6, 30e-6, 90e-6]

# We loop through the three radii and the three subplots
for radius, ax in zip(radii, axes):

    # During each loop we change the radius in the model
    yosioka.R_0 = radius

    # We plot the wireframe plot in the respect
    wireframe_plot = osaft.ParticleWireframePlot(yosioka, scale_factor=0.1)
    wireframe_plot.plot(ax=ax)

    # Making the plot prettier
    um_r = int(yosioka.R_0 * 1e6)
    ax.axis(False)
    ax.set_aspect(1)
    ax.set_title(rf"$R_0 = {{{um_r}}}\mathrm{{\mu m}}$")

fig.tight_layout()
plt.show()
