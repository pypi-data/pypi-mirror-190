"""
Multicore ARF Computation
=========================

In this example we show how multiprocessing can be used to improving
computation speed for ARF plots.
"""

# %%
# For computationally expensive models, i.e. models that include numerical
# integration the OSAFT library provides the option for computing the ARF
# using multiprocessing. If a solution class is added to an ``ARFPlot``
# instance using ``add_solutions`` the parameter ``multicore`` can be set to
# ``True``. Now the computation of the ARF for each point of the plot will be
# computed in a new process that will run in parallel.
#
# The models used in the example below should probably not be used with the
# ``multicore`` option, since they are simple and evaluate very fast. For
# simple models multiprocessing will not lead to faster evaluation.
#
#
# **Important**
#
# In order for multiprocessing to work you need to run your code in your main
# file inside the ``if __name__ == '__main__':`` clause as shown below.
# Check the
# `multiprocessing documentation
# <https://docs.python.org/3/library/multiprocessing.html>`_ for more
# information.


import numpy as np
from matplotlib import pyplot as plt

import osaft


def main():

    king = osaft.king1934.ARF(
        f=1e6,
        R_0=1e-6,
        rho_s=1020,
        rho_f=997,
        c_f=1498,
        p_0=1e5,
        wave_type=osaft.WaveType.STANDING,
        position=osaft.pi / 4,
    )

    yosioka = osaft.yosioka1955.ARF(
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

    gorkov = osaft.gorkov1962.ARF(
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

    plot = osaft.ARFPlot("R_0", np.linspace(1e-6, 20e-6))

    # Solutions added using multiprocessing
    plot.add_solutions(king, yosioka, multicore=True)

    # Solutions added without multiprocessing
    plot.add_solutions(gorkov)

    plot.plot_solutions()

    plt.show()


if __name__ == "__main__":
    main()
