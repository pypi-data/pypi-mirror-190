"""
Pressure Plots for different theories
=====================================

This example shows how to plot the pressure field for different theories
in one single figure.
"""

# %%
# In this example we are investigating a polystyrene particle in a viscous
# oil in a standing wave.

from matplotlib import pyplot as plt

import osaft

# --------
# Geometry
# --------
# Radius
R_0 = 5e-6  # [m]

# -------------------------
# Properties of polystyrene
# -------------------------
# Density
rho_ps = 1_050  # [kg/m^3]
# Young's modulus
E_ps = 3.25e9  # [Pa]
# Poisson's ratio
nu_ps = 0.34  # [-]
# Speed of sound (matching compressibility)
c_ps = (E_ps / (rho_ps * 3 * (1 - 2 * nu_ps))) ** 0.5  # [m/s]

# -------------------
# Properties of Oil
# -------------------
# Density
rho_oil = 923  # [kg/m^3]
# Speed of sound
c_oil = 1_445  # [m/s]
# Viscosity
eta_oil = 0.03  # [Pa s]
zeta_oil = 0  # [Pa s]

# --------------------------------
# Properties of the Acoustic Field
# --------------------------------
# Frequency
f = 1e6  # [Hz]
# Pressure
p_0 = 1e5  # [Pa]
# Wave type
wave_type = osaft.WaveType.STANDING
# position
position = osaft.pi / 4

# %%
# Once all properties are defined we can initialize the solution instances for
# the scattering field. We also save the solutions to a list which will make
# looping in the next steps straightforward.

solutions = []

solutions.append(
    osaft.king1934.ScatteringField(
        f=f,
        R_0=R_0,
        rho_s=rho_ps,
        rho_f=rho_oil,
        c_f=c_oil,
        p_0=p_0,
        wave_type=wave_type,
        position=position,
    ),
)


solutions.append(
    osaft.yosioka1955.ScatteringField(
        f=f,
        R_0=R_0,
        rho_s=rho_ps,
        c_s=c_ps,
        rho_f=rho_oil,
        c_f=c_oil,
        p_0=p_0,
        wave_type=wave_type,
        position=position,
    ),
)

solutions.append(
    osaft.hasegawa1969.ScatteringField(
        f=f,
        R_0=R_0,
        rho_s=rho_ps,
        E_s=E_ps,
        nu_s=nu_ps,
        rho_f=rho_oil,
        c_f=c_oil,
        p_0=p_0,
        wave_type=wave_type,
        position=position,
    ),
)

solutions.append(
    osaft.doinikov1994rigid.ScatteringField(
        f=f,
        R_0=R_0,
        rho_s=rho_ps,
        rho_f=rho_oil,
        c_f=c_oil,
        eta_f=eta_oil,
        zeta_f=zeta_oil,
        p_0=p_0,
        wave_type=wave_type,
        position=position,
    ),
)

# %%
# The next step is to initialise the plotter. We need a separate plotter for
# all solutions. We can now make use of the list of solutions. The respective
# plotters will be saved in a dictionary where the key is the name of
# the solution.

plotter = {}
for solution in solutions:
    plotter[solution.name] = osaft.FluidScatteringPlot(
        solution,
        r_max=5 * solution.R_0,
    )


# %%
# Now we initialise an empty figure with four subplots and pass the
# ``plt.Axes`` object to the plotting function. Additionally, we will also
# change the title of the subplot.


fig, axes = plt.subplots(
    nrows=2,
    ncols=2,
    figsize=(10, 10),
    sharex=True,
    sharey=True,
)

count = 0
for name, plotter in plotter.items():
    ax = axes.flat[count]
    plotter.plot_pressure(
        inst=True,
        incident=False,
        scattered=True,
        ax=ax,
    )
    ax.set_title(name)

    # remove the y and x label for non-boundary subplots
    if count == 0:  # top left
        ax.set_xlabel("")
    elif count == 1:  # top right
        ax.set_xlabel("")
        ax.set_ylabel("")
    elif count == 3:  # bottom right
        ax.set_ylabel("")

    count += 1

fig.tight_layout()
plt.show()
