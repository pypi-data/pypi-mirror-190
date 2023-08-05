"""
Acoustofluidics 2022: Plotting the Scattering Field
====================================================
This example is from the presentation at the Acoustofluidics 2022 conference
and shows how to plot the scattered pressure field and the mode shape of a
polystyrene particle suspended in water and subjected to a 5MHz-standing wave.
"""

# %%
# We import ``osaft`` and initialise the model with parameters of the
# polystyrene particle, water, and the acoustic field.

from matplotlib import pyplot as plt

import osaft

hasegawa = osaft.hasegawa1969.ScatteringField(
    f=5e6,
    R_0=1e-6,
    rho_s=1020,
    E_s=3.4e9,
    nu_s=0.4,
    rho_f=1498,
    c_f=997,
    p_0=1e5,
    wave_type=osaft.WaveType.STANDING,
    position=osaft.pi / 4,
)

# %%
# We generate the particle animation for the small 1-micron particle. It can
# be seen how its motion is dominated by the dipole mode.

plot_particle_small = osaft.ParticleWireframePlot(hasegawa)
anim_particle_small = plot_particle_small.animate()
plt.show()

# %%
# Also the scattered pressure field is dominated by the contribution of
# the dipole mode.

plot_fluid_small = osaft.FluidScatteringPlot(hasegawa, r_max=5 * hasegawa.R_0)
anim_fluid_small = plot_fluid_small.animate_pressure(incident=False)
plt.show()

# %%
# We increase the particle radius and we animate the particle motion of the
# 50-micron particle analogously to the small particle.

hasegawa.R_0 = 50e-6

plot_particle_large = osaft.ParticleWireframePlot(hasegawa)
anim_fluid_large = plot_particle_large.animate()
plt.show()

# %%
# For the large particle both particle motion and scattered pressure field
# are dominated by the quadrupole mode, i.e. a mode neglected in most
# theories only considering the long-wavelength limit.

plot_fluid_large = osaft.FluidScatteringPlot(hasegawa, r_max=5 * hasegawa.R_0)
anim_particle_large = plot_fluid_large.animate_pressure(incident=False)
plt.show()
