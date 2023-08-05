from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from osaft.plotting.base_plotting import BasePlot
from osaft.plotting.datacontainers.arf_datacontainer import ARFData

NDArray = np.ndarray


class ARFPlotter(BasePlot):
    def __init__(self) -> None:
        self._abscissa = None
        self._attr_name = None

    def plot_solution(
        self,
        x_values: NDArray,
        data: ARFData,
        ax: plt.Axes,
        plot_method,
        **kwargs,
    ) -> (plt.Figure, plt.Axes):
        """plot_solution.

        :param x_values: abscissa data
        :param data: data to plot
        :param ax: axis object
        :param plot_method: plotting method to use
        :param kwargs: keyword arguments piped to :attr:`plot_method`
        """
        fig, ax = self._create_figure(ax)

        keys = kwargs.keys()
        if "ls" not in keys and "linestyle" not in keys:
            kwargs["linestyle"] = data.line_style

        plt.sca(ax)
        plot_method(
            x_values,
            data.plotting,
            label=data.name,
            **kwargs,
        )

        return fig, ax

    @staticmethod
    def add_legend(ax: plt.Axes) -> None:
        """Adds a legend to the given axis object

        :param ax:
        """
        ax.legend()

    @staticmethod
    def set_labels(
        ax: plt.Axes,
        attr_name: str,
        is_normalized: None | bool = False,
    ) -> None:
        """Sets the labels for both plotting axis

        :param ax: axis to work on
        :param attr_name: name of attribute on abscissa
        :param is_normalized: plotting of normalized solution
        """
        ax.set_xlabel(f"Attribute {attr_name}")

        if is_normalized:
            ax.set_ylabel("normalized ARF [-]")
        else:
            ax.set_ylabel(r"$F^{\mathrm{rad}}$ $\mathrm{[N]}$")


if __name__ == "__main__":
    pass
