"""
Possible Numerical Problems
=====================================

As with an numerical software, it is possible that the numerics run into
problems for certain set of parameters. Luckily, for the usual range of
parameters relevant in acoustofluidics there seem to be few problems in OSAFT.
In our automated tests, we test every model in this relevant parameter range.
Nevertheless, it is still possible to run into numerical problems. In this
example, we show when these problems could arise and how they can be dealt
with.

In this example we investigate a heavy particle in a highly viscous
fluid. We are using the model ``doinikov1994rigid``. For high
viscosities ( :math:`\\eta_f \\approx 0.5 \\mathrm{Pa s}`) and very small
particles (:math:`R_0= 500\\mathrm{nm}`) this solution can become unstable.
We are comparing the general solution of this model with the long
wavelength approximation.
"""
import numpy as np
from matplotlib import pyplot as plt

import osaft

general = osaft.doinikov1994rigid.ARF(
    f=1e5,
    R_0=5e-7,
    rho_s=5e4,
    rho_f=1e3,
    c_f=1500,
    eta_f=1e-3,
    zeta_f=0,
    p_0=1e5,
    wave_type=osaft.WaveType.STANDING,
    position=osaft.pi / 4,
)

approx = general.copy()
approx.long_wavelength = True

general.name = "General"
approx.name = "Long Wavelength"

# %%
# The ARF on the particle is computed for different values of viscosity. The
# general solution becomes unstable as we pass a viscosity of
# :math:`\eta_f \approx 0.1 \mathrm{Pa s}` the solution becomes unstable.
# In order for multiprocessing to work you need to run your code inside the
# ``if __name__ == '__main__':`` clause as shown below.
# Check the
# :ref:`multiprocessing example
# <sphx_glr_examples_tutorial_example_multicore.py>`.

if __name__ == "__main__":

    arf_plot = osaft.ARFPlot("eta_f", np.logspace(-3, -0.5, num=16))
    arf_plot.add_solutions(approx, multicore=False)
    arf_plot.add_solutions(general, multicore=True)

    fig, ax = arf_plot.plot_solutions(plot_method=plt.semilogx, marker="o")
    ax.set_xlabel("$\\eta_f$ $\\mathrm{[Pa s]}$")
    plt.show()

    print(f"{approx.eta_f = }")
    print(f"{abs(approx.x):.3e} << 1")
    print(f"{abs(approx.x):.3e} << {abs(approx.x_v):.3e}")

# %%
# If one runs into numerical issues, the easiest remedy is to choose a
# different model or a different approximation of a model. In this case here
# the ``long_wavelength`` solution seems to be more suitable. In particular,
# since the assumption of a long wavelength, i.e.
# :math:`x \ll 1`, :math:`x \ll x_v`, still holds. We can confirm this
# easily using the OSAFT library.
