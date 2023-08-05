"""
Frontiers: PS Particle in Water
===============================

This example corresponds to section 3.1 in
:ref:`our publication <CitingOsaft>`.
In this example we compute the acoustic radiation force (ARF) on a polystyrene
particle suspended in water subjected to a plane standing wave. We compare
the theories from Yosioka & Kawasima (1955), Gor'kov (1962), and Settnes &
Bruus (2012).
"""

# %%
# As always we start off by importing the nececassry Python modules. For this
# example we are only going to need the osaft library.

import osaft

# %%
# The next step is to define the properties for our example,
# these include the material properties, the properties of the acoustic field,
# and the radius of the particle. In the osaft library we are always
# assuming SI-units.
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

# -------------------
# Properties of Water
# -------------------
# Speed of sound
c_f = 1_498  # [m/s]
# Density
rho_f = 997  # [kg/m^3]
# Viscosity at 25 degC
eta_w = 0.89e-3  # [Pa s]

# -------------------------
# Properties of Polystyrene
# -------------------------
# Speed of sound
c_s = 2350  # [m/s]
# Density
rho_s = 1020  # [kg/m^3]

# --------------------------------
# Properties of the Acoustic Field
# --------------------------------
# Frequency
f = 1e5  # [Hz]
# Pressure
p_0 = 1e5  # [Pa]
# Wave type
wave_type = osaft.WaveType.STANDING
# Position of the particle in the field
position = osaft.pi / 4  # [rad]

# %%
# Once all properties are defined we can initialize the solution classes.
# In this example, we use the classes ``osaft.yosioka1955.ARF()``,
# ``osaft.gorkov1962.ARF()``, and ``osaft.settnes2012.ARF()``.

yosioka = osaft.yosioka1955.ARF(
    f=f,
    R_0=R_0,
    rho_s=rho_s,
    c_s=c_s,
    rho_f=rho_f,
    c_f=c_f,
    p_0=p_0,
    wave_type=wave_type,
    position=position,
)

gorkov = osaft.gorkov1962.ARF(
    f=f,
    R_0=R_0,
    rho_s=rho_s,
    c_s=c_s,
    rho_f=rho_f,
    c_f=c_f,
    p_0=p_0,
    wave_type=wave_type,
    position=position,
)

settnes = osaft.settnes2012.ARF(
    f=f,
    R_0=R_0,
    rho_s=rho_s,
    c_s=c_s,
    rho_f=rho_f,
    c_f=c_f,
    eta_f=eta_w,
    p_0=p_0,
    wave_type=wave_type,
    position=position,
)

# %%
# Now we want to make sure that the solutions from Gor'kov and Settnes &
# Bruus are actually applicable. These theories assume a small particle
# compared to the acoustic wavelength
#
# .. math::
#  k_\mathrm{f} \cdot R_0 \ll 1
#
# We evaluate this expression using osaft

print(f"{yosioka.k_f * yosioka.R_0 = :.4f}")

# %%
# And indeed, we were able to confirm that this is the case.
#
# Finally, we compute the acoustic radiation force for all models by calling
# the ``compute_arf()`` method on all instances.

print(f"{yosioka.compute_arf() = :.3e}")
print(f"{gorkov.compute_arf() = :.3e}")
print(f"{settnes.compute_arf() = :.3e}")


# %%
# We have found that all solutions are in excellent agreement.
