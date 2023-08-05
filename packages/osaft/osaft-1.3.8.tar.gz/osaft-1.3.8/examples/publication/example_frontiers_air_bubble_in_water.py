"""
Frontiers: Air Bubble in Water
==============================

This example corresponds to section 3.4 in
:ref:`our publication <CitingOsaft>`.
In this example we study the acoustic radiation force (ARF) on an air bubble
suspended in water.
"""

# %%
# As always we start off by importing the necessary Python modules. For our
# example we are going to need the osaft library, and the third party packages
# NumPy and Matplotlib.

import numpy as np
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
# Properties of Air
# -----------------
# Speed of sound
c_air = 343  # [m/s]
# Density
rho_air = 1.225  # [kg/m^3]

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
position = np.pi / 4  # [rad]

# %%
# Once all properties are defined we can initialize the solution instances.
# ``osaft.yosioka1995.ARF()`` is the class for computing the ARF using the
# model by Yosioka and Kawasima (1955).
#
# Here we give the instances different names ``'General'`` and ``'Bubble'``
# by setting the ``name`` attribute.
# This makes sure we can later distinguish them when the solutions are plotted.

# General
yosioka = osaft.yosioka1955.ARF(
    f=f,
    R_0=R_0,
    rho_s=rho_air,
    c_s=c_air,
    rho_f=rho_w,
    c_f=c_w,
    p_0=p_0,
    wave_type=wave_type,
    position=position,
)
yosioka.name = "General"

# Small bubble approximation
yosioka_bubble = yosioka.copy()
yosioka_bubble.small_particle = True
yosioka_bubble.bubble_solution = True
yosioka_bubble.name = "Bubble"

# %%
# With the class ``osaft.yosioka1955.ARF()`` it is also possible to plot the
# acoustic fields. Here, we first set the frequency to ``6.5e5`` Hz.
# Then we initialize a ``osaft.FluidScatteringPlot()`` instance which will plot
# the acoustic field in the fluid. The class takes the model as an argument
# and the radius range ``r_max`` that is plotted. For more option see the
# documentation.
#
# The method ``plot()`` will then generate the plot.
# As always with Matplotlib, we need to call ``plt.show()`` to display it.

# Setting frequency close to resonance
yosioka.f = 6.5e5

# Initializing plotting class
scattering_plot = osaft.FluidScatteringPlot(yosioka, r_max=3 * yosioka.R_0)

# Plot scattering field
fig, ax = scattering_plot.plot_velocity()

plt.show()

# %%
# To animate the acoustic field we can call the method
# ``animate()``. Setting
# ``incident = False`` means that we are only animating the scattered field
# but not the incident field.

anim = scattering_plot.animate_velocity(
    frames=20,
    interval=100,
    incident=False,
)

plt.show()

# %%
# Finally, we want to compare the general solution for the ARF
# with the approximate solution for a bubble. To plot the ARF
# we need to initialize ``osaft.ARFPlot()`` instance. With the method
# ``add_solutions()`` we can add our models to the plotter.
# With ``set_abscissa()`` we define the variable that we want to
# plot the ARF against. Here we select the frequency ``f``.
# Finally, ``osaft.ARFPlot.plot_solutions()`` will generate the plot. Again,
# we call ``plt.show()`` to display it.

# sphinx_gallery_thumbnail_number = -1
# Initializing plotting class
arf_plot = osaft.ARFPlot()

# Add solutions to be plotted
arf_plot.add_solutions(yosioka, yosioka_bubble)

# Define independent plotting variable (in this case the frequency)
arf_plot.set_abscissa(x_values=np.linspace(1e5, 1e6, 300), attr_name="f")

# Plot the ARF
fig, ax = arf_plot.plot_solutions()

# Setting the axis labels
ax.set_xlabel(r"$f$ $\mathrm{[Hz]}$")

plt.show()

# %%
# .. note::
#       It is only possible to plot the ARF  against
#       properties that wrap an underlying ``PassiveVariable``, i.e. an input
#       parameter of the model.
#       You can get a list of all input variables using the method
#       ``input_variables()``.

print(f"{yosioka.input_variables() = }")
