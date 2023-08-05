"""
Acoustofluidics 2022: Minimal Example Plotting Scattering Fields
===============================================================
This is the minimal example on how to plot the scattered pressure field around
a polystyrene particle suspended in water and subjected to an acoustic standing
wave from the abstract book from the Acoustofluidics 2022 conference.
"""

# %%
# We import ``osaft`` and initialise the model from Yosioka & Kawasima.

from matplotlib import pyplot as plt

import osaft

yosioka = osaft.yosioka1955.ScatteringField(
    f=1e6,
    R_0=1e-6,
    rho_s=1020,
    c_s=2350,
    rho_f=997,
    c_f=1498,
    p_0=1e5,
    wave_type=osaft.WaveType.STANDING,
    position=osaft.pi / 4,
)

# %%
# The model is passed to the plotting class and the pressure field is
# plotted. The option ``incident=False`` makes sure that only the
# scattered field is plotted but not the incident field.

plot = osaft.FluidScatteringPlot(yosioka, r_max=4e-6)

plot.plot_pressure(incident=False)

plt.show()
