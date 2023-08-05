"""
Hasegawa (1979) Figure 3
========================
In this example we recreate Figure 3 from Hasegawa's 1979 paper.
"""

# %%
# First, we need to get an instance of our solution class. In this case
# ``osaft.hasegawa1969.ARF()``. The steps are the same as in the earlier
# examples. Note that we set ``N_max = 12``. ``N_max`` is the highest
# vibration mode of the sphere still considered in the computation.
# In this example we need to consider many modes since
# the wavelength is of similar length as the particle diameter.
# This is usually not the case and the default value of ``N_max = 5`` is
# more than sufficient to get an accurate value for the ARF.

import matplotlib.pyplot as plt
import numpy as np

import osaft

# --------
# Geometry
# --------
# Radius
R_0 = 1e-6  # [m]

# ----------------------------
# Properties of Brass Particle
# ----------------------------
rho_s = 8100  # [kg/m^3]
E_s = 88e9  # [Pa]
nu_s = 0.301  # [-]
# -------------------
# Properties of Water
# -------------------
rho_f = 1000  # [kg/m^3]
c_f = 1500  # [m/s]

# --------------------------------
# Properties of the Acoustic Field
# --------------------------------
pos = osaft.pi / 4
f = 1e6
p_0 = 1e5
wave_type = osaft.WaveType.STANDING
N_max = 12

hasegawa = osaft.hasegawa1969.ARF(
    rho_s=rho_s,
    E_s=E_s,
    nu_s=nu_s,
    rho_f=rho_f,
    c_f=c_f,
    position=pos,
    f=f,
    R_0=R_0,
    p_0=p_0,
    wave_type=wave_type,
    N_max=N_max,
)

# %%
# We need to plot the ARF over a range of values of :math:`k_f R_0`. For
# this we are changing the radius :math:`R_0` while keeping all other
# parameters constant.

N = 100
R_min = 1e-6
R_max = 10 / hasegawa.k_f
R0_values = np.linspace(R_min, R_max, N)
kr_values = hasegawa.k_f * R0_values

# %%
# Here we initiate the plot and add the solution.
# In the first argument (``x_values``) we define the values for
# which the second argument (``attr_name``) should be evaluated.

arf_plot = osaft.ARFPlot(x_values=R0_values, attr_name="R_0")
arf_plot.add_solutions(hasegawa)

# %%
# In his article Hasegawa does not plot the ARF itself but normalized it
# w.r.t. to the acoustic energy density and the cross-sectional area of the
# sphere.
#
# .. math::
#   Y_\text{ST} = (F^\text{rad} / \pi R_0^2 E_\text{ac})
#
# We therefore define a normalization function that depends on our variable
# ``R_0`` that we are going to plot the ARF over and we will later pass it
# to ``plot_solutions``.
# Note that the factor of ``1/2`` stems from the fact that Hasegawa has
# defined the energy w.r.t. to a single propagating wave and not the overall
# pressure amplitude of the standing wave.


def normalization(radius):
    return 1 / 2 * hasegawa.field.E_ac * osaft.pi * radius**2


# %%
# Finally, we plot the figure. Here we use ``plt.subplots()`` to get a figure
# with the correct aspect ratio and pass the ``Axes`` instance ``ax`` to
# ``plot_solutions``.
# We can directly pass ``display_values`` to the ``plot_solutions`` method,
# in order to plot over the values of :math:`k_f R_0` instead of the radius.

fig, ax = plt.subplots(figsize=(3, 5))
arf_plot.plot_solutions(
    ax=ax,
    display_values=kr_values,
    color="black",
    normalization=normalization,
)
ax.set_xlabel(r"$ka$")
ax.set_ylabel("$Y_{ST}$")
ax.axhline(0, color="k")
ax.set_xlim(left=0, right=10)
ax.set_ylim(bottom=-1, top=3.5)
ax.set_xticks([0, 2, 4, 6, 8])
ax.set_yticks([-1, 0, 1, 2, 3])
ax.legend(["Brass"])
fig.tight_layout()
plt.show()
