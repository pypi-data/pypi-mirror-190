r"""
Doinikov Rigid (1994): Sandstone in Glycerin
============================================
6.b.ii. Doinikov compute the acoustic radiation force on a sandstone
particle in water and in glycerin. Doinikov shows that the acoustic
radiation force will change sign in the case :math:`|x| \ll |x_v| \ll 1`,
i.e. if the particle and the viscous boundary layer are small compared to
the wavelength and the boundary layer is much larger than the particle.
"""

# %%
# First we need to get an instance of our solution class. In this case
# ``osaft.king1934.ARF()`` and ``osaft.doinikov1994rigid.ARF()``. The steps are
# the same as in the earlier examples.

import matplotlib.pyplot as plt
import numpy as np

import osaft

# --------
# Geometry
# --------
# Radius
R_0 = 1e-6  # [m]

# -----------------------
# Properties of Sandstone
# -----------------------
# Density
rho_sandstone = 7.8e3  # [kg/m^3]

# ----------------------
# Properties of Glycerin
# ----------------------
# Speed of sound
c_glycerin = 1_964  # [c/m]
# Density
rho_glycerin = 1.26e3  # [kg/m^3]
# dynamic viscosity
eta_glycerin = 0.950  # [Pa s]


# -------------------
# Properties of Water
# -------------------
# Speed of sound
c_water = 1_492  # [m/s]
# Density
rho_water = 997  # [kg/m^3]
# dynamic viscosity
eta_water = 8.9e-4  # [Pa s]

# --------------------------------
# Properties of the Acoustic Field
# --------------------------------
# Frequency
f = 1e6  # [Hz]
# Pressure
p_0 = 1e5  # [Pa]
# Wave type
wave_type = osaft.WaveType.STANDING

# Theory of Doinikov with glycerin as medium
D_glycerin = osaft.doinikov1994rigid.ARF(
    f=f,
    R_0=R_0,
    rho_s=rho_sandstone,
    rho_f=rho_glycerin,
    c_f=c_glycerin,
    eta_f=eta_glycerin,
    zeta_f=0,
    p_0=p_0,
    wave_type=wave_type,
    position=0,
    long_wavelength=True,
    large_boundary_layer=True,
)
D_glycerin.name = "Doinikov: Glycerin"

# Theory of Doinikov with water as medium
D_water = osaft.doinikov1994rigid.ARF(
    f=f,
    R_0=R_0,
    rho_s=rho_sandstone,
    rho_f=rho_water,
    c_f=c_water,
    eta_f=eta_water,
    zeta_f=0,
    p_0=p_0,
    wave_type=wave_type,
    position=0,
)
D_water.name = "Doinikov: Water"

# Theory of King with glycerin as medium
K_glycerin = osaft.king1934.ARF(
    f=f,
    R_0=R_0,
    rho_s=rho_sandstone,
    rho_f=rho_glycerin,
    c_f=c_glycerin,
    p_0=p_0,
    wave_type=wave_type,
    position=0,
    small_particle_limit=True,
)
K_glycerin.name = "King: Glycerin"

# Theory of King with water as medium
K_water = K_glycerin.copy()
K_water.rho_f = rho_water
K_water.c_f = c_water
K_water.name = "King: Water"

# %%
# We plot the acoustic radiation force by initializing an instance of
# ``osaft.ARFPlot()`` and adding our solutions using ``add_solutions()``.

# create the x values we want to use for plotting
x_values = np.linspace(0, np.pi, num=500)

# Plotting the solutions
plotter = osaft.ARFPlot("position", x_values)
plotter.add_solutions(D_water, D_glycerin, K_water, K_glycerin)
plotter.plot_solutions()

plt.show()
