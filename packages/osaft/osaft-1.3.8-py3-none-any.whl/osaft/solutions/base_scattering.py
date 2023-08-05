from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Sequence

import numpy as np

from osaft import BackgroundField
from osaft.core.functions import BesselFunctions as Bf
from osaft.core.functions import LegendreFunctions as Leg
from osaft.core.functions import cos, exp, full_range, sin
from osaft.core.helper import InputHandler
from osaft.core.variable import PassiveVariable

NDArray = np.ndarray


class BaseScattering(ABC):
    """Base class for the scattering field that defines the common
    interface.

    .. note::
       This base class can be used for axisymmetric models only.

    :param N_max: End of the infinite series for the scattering coefficients
    """

    # Required properties by child class

    field: BackgroundField  # Background field instance
    omega: float  # Angular frequency
    R_0: float  # Radius
    rho_f: float  # Fluid density
    k_f: float  # Fluid wavenumber

    def __init__(self, N_max: int = 5) -> None:
        """Constructor method"""

        # Independent variables
        self._N_max = PassiveVariable(N_max, "number of modes N")

    # -------------------------------------------------------------------------
    # API - Acoustic Velocity and Displacement
    # -------------------------------------------------------------------------

    def radial_acoustic_fluid_velocity(
        self,
        r: float | Sequence,
        theta: float | Sequence,
        t: float | Sequence,
        scattered: bool,
        incident: bool,
        mode: None | int = None,
    ) -> complex | NDArray:
        """Returns the value for the radial acoustic velocity in [m/s].

        This method must be implemented by every theory to have a common
        interface for other modules.

        :param r: radial coordinate [m]
        :param theta: tangential coordinate [rad]
        :param t: time [s]
        :param scattered: scattered field contribution
        :param incident: incident field contribution
        :param mode: specific mode number of interest; if `None` then all
                     modes until :attr:`.N_max`
        """

        def radial_func(m: int, s: float) -> complex:
            return self.V_r(m, s, scattered=scattered, incident=incident)

        r, theta, t = InputHandler.handle_input(
            r,
            theta,
            t,
            self.R_0,
            inside_sphere=False,
        )
        out = self.radial_mode_superposition(
            radial_func,
            r,
            theta,
            t,
            mode,
        )

        return out

    def tangential_acoustic_fluid_velocity(
        self,
        r: float | Sequence,
        theta: float | Sequence,
        t: float | Sequence,
        scattered: bool,
        incident: bool,
        mode: None | int = None,
    ) -> complex | NDArray:
        """Returns the value for the tangential acoustic velocity in [m/s].

        This method must be implemented by every theory to have a common
        interface for other modules.

        :param r: radial coordinate [m]
        :param theta: tangential coordinate [rad]
        :param t: time [s]
        :param scattered: scattered field contribution
        :param incident: incident field contribution
        :param mode: specific mode number of interest; if `None` then all
                     modes until :attr:`.N_max`
        """

        def radial_func(m: int, s: float) -> complex:
            return self.V_theta(m, s, scattered=scattered, incident=incident)

        r, theta, t = InputHandler.handle_input(
            r,
            theta,
            t,
            self.R_0,
            inside_sphere=False,
        )

        out = self.tangential_mode_superposition(
            radial_func,
            r,
            theta,
            t,
            mode,
        )

        return out

    def pressure(
        self,
        r: float | Sequence,
        theta: float | Sequence,
        t: float | Sequence,
        scattered: bool,
        incident: bool,
        mode: None | int = None,
    ) -> complex:
        """Returns the acoustic pressure [Pa].

        :param r: radial coordinate [m]
        :param theta: tangential coordinate [rad]
        :param t: time [s]
        :param scattered: add scattered field
        :param incident: add incident
        :param mode: specific mode number of interest; if `None` then all
                     modes until :attr:`.N_max`
        """
        r, theta, t = InputHandler.handle_input(
            r,
            theta,
            t,
            self.R_0,
            inside_sphere=False,
        )

        out = -1j * self.omega * self.rho_f
        out *= self.velocity_potential(r, theta, t, scattered, incident, mode)

        return out

    @abstractmethod
    def potential_coefficient(self, n: int) -> complex:
        """Wrapper to the fluid scattering coefficients for an inviscid fluid

        This method must be implemented by every theory to have a common
        interface for other modules.

        :param n: mode
        """
        pass

    def velocity_potential(
        self,
        r: float | Sequence,
        theta: float | Sequence,
        t: float | Sequence,
        scattered: bool,
        incident: bool,
        mode: None | int = None,
    ) -> complex:
        """Returns the velocity potential of the fluid in [m^2/s].

        :param r: radial coordinate [m]
        :param theta: tangential coordinate [rad]
        :param t: time [s]
        :param scattered: add scattered field
        :param incident: add incident
        :param mode: specific mode number of interest; if `None` then all
                     modes until :attr:`.N_max`
        """
        r, theta, t = InputHandler.handle_input(
            r,
            theta,
            t,
            self.R_0,
            inside_sphere=False,
        )

        if not scattered and not incident:
            raise ValueError(
                "Neither scattered nor incident field has "
                "been has been selected. Velocity field is zero.",
            )
        elif scattered and incident:

            def inner_func(m: int, s: float):
                x = self.k_f * s
                potential = self.field.A_in(m) * Bf.besselj(m, x)
                potential += self.potential_coefficient(m) * Bf.hankelh1(m, x)
                return potential

        elif scattered and not incident:

            def inner_func(m: int, s: float):
                x = self.k_f * s
                return self.potential_coefficient(m) * Bf.hankelh1(m, x)

        else:

            def inner_func(m: int, s: float):
                x = self.k_f * s
                return self.field.A_in(m) * Bf.besselj(m, x)

        if mode is None:
            out = self.radial_mode_superposition(inner_func, r, theta, t, mode)
        else:
            out = Leg.cos_monomial(mode, theta, inner_func(mode, r)) * exp(
                -1j * self.omega * t,
            )

        return out

    @abstractmethod
    def radial_particle_velocity(
        self,
        r: float | Sequence,
        theta: float | Sequence,
        t: float | Sequence,
        mode: None | int = None,
    ) -> complex:
        """Returns the value for the radial particle velocity in [m/s].

        This method must be implemented by every theory to have a common
        interface for other modules.

        :param r: radial coordinate [m]
        :param theta: tangential coordinate [rad]
        :param t: time [s]
        :param mode: specific mode number of interest; if `None` then all
                     modes until :attr:`.N_max`
        """
        pass

    @abstractmethod
    def tangential_particle_velocity(
        self,
        r: float | Sequence,
        theta: float | Sequence,
        t: float | Sequence,
        mode: None | int = None,
    ) -> complex:
        """Returns the value for the tangential particle velocity in [m/s].

        This method must be implemented by every theory to have a common
        interface for other modules.

        :param r: radial coordinate [m]
        :param theta: tangential coordinate [rad]
        :param t: time [s]
        :param mode: specific mode number of interest; if `None` then all
                     modes until :attr:`.N_max`
        """
        pass

    def radial_particle_displacement(
        self,
        r: float | Sequence,
        theta: float | Sequence,
        t: float | Sequence,
        mode: None | int = None,
    ) -> complex | NDArray:
        """Particle displacement in radial direction

        Returns the value of the particle displacement
        in radial direction in [m]

        :param r: radial coordinate [m]
        :param theta: tangential coordinate [rad]
        :param t: time [s]
        :param mode: specific mode number of interest; if `None` that all
                     modes until :attr:`.N_max`
        """
        velocity = self.radial_particle_velocity(r, theta, t, mode)
        return velocity / (-1j * self.omega)

    def tangential_particle_displacement(
        self,
        r: float | Sequence,
        theta: float | Sequence,
        t: float | Sequence,
        mode: None | int = None,
    ) -> complex | NDArray:
        """Particle displacement in tangential direction

        Returns the value of the particle displacement
        in tangential direction in [m]

        :param r: radial coordinate [m]
        :param theta: tangential coordinate [rad]
        :param t: time [s]
        :param mode: specific mode number of interest; if `None` that all
                     modes until :attr:`.N_max`
        """
        velocity = self.tangential_particle_velocity(r, theta, t, mode)
        return velocity / (-1j * self.omega)

    # -------------------------------------------------------------------------
    # Getters and Setters
    # -------------------------------------------------------------------------

    @property
    def N_max(self):
        """Cutoff mode number for infinite sums

        :getter: returns number of infinite sum term
        :setter: automatically invokes
            :meth:`osaft.core.variable.BaseVariable.notify`
        """
        return self._N_max.value

    @N_max.setter
    def N_max(self, value):
        self._N_max.value = value

    # -------------------------------------------------------------------------
    # Mode Superposition
    # -------------------------------------------------------------------------

    def radial_mode_superposition(
        self,
        radial_func: Callable[[int, float], complex],
        r: float | Sequence,
        theta: float | Sequence,
        t: float | Sequence,
        mode: int = None,
    ) -> complex | NDArray:
        """Returns either a single mode (``mode=int``) or a the sum until
        :attr:`.N_max` (``mode=None``).

        If ``mode=int`` the formula is

        .. math::
           e^{-i\\omega t}\\,
           f_{\\text{mode}}(r)
           \\,P_{\\text{mode}}(\\cos\\theta)

        If ``mode=None`` the formula is

        .. math::
           e^{-i\\omega t} \\sum_{n=0}^{\\text{N}_{\\text{max}}}
           \\,f_n(r)
           \\,P_n(\\cos\\theta)


        where :math:`f_\\text{n}(r)` is the ``radial_func(n, r)``
        passed to the method.

        :param radial_func: radial function dependent on :attr:`r`
        :param r: radial coordinate [m]
        :param theta: tangential coordinate [rad]
        :param t: time [s]
        :param mode: specific mode number of interest; if `None` then all
                     modes until :attr:`.N_max`
        """

        out = exp(-1j * self.omega * t)
        if mode is not None:
            out *= Leg.cos_monomial(mode, theta, radial_func(mode, r))
        else:
            out *= Leg.cos_poly(
                theta,
                np.array(
                    [radial_func(n, r) for n in full_range(0, self.N_max)],
                ),
            )
        return out

    def tangential_mode_superposition(
        self,
        tangential_func: Callable[[int, float], complex],
        r: float | Sequence,
        theta: float | Sequence,
        t: float | Sequence,
        mode: int,
    ) -> complex | NDArray:
        """Returns either a single mode (``mode=int``) or a the sum until
        :attr:`.N_max` (``mode=None``).

        If ``mode=int`` the formula is

        .. math::
           e^{-i\\omega t}\\,
           f_\\text{mode}(r)
           \\,P^1_{\\text{mode}}(\\cos\\theta)

        If ``mode=None`` the formula is

        .. math::
           e^{-i\\omega t}\\sum_{n=0}^{\\text{N}_{\\text{max}}}
           \\,f_n(r)
           \\,P^1_n(\\cos\\theta)


        where :math:`f_n(r)` is the ``tangential_func(n, r)``
        passed to the method.

        :param tangential_func: tangential function dependent on :attr:`r`
        :param r: radial coordinate [m]
        :param theta: tangential coordinate [rad]
        :param t: time [s]
        :param mode: specific mode number of interest; if `None` then all
                     modes until :attr:`.N_max`
        """

        out = exp(-1j * self.omega * t)
        if mode is not None:
            out *= Leg.first_cos_monomial(
                mode,
                theta,
                tangential_func(mode, r),
            )
        else:
            out *= Leg.first_cos_poly(
                theta,
                np.array(
                    [tangential_func(n, r) for n in full_range(0, self.N_max)],
                ),
            )
        return out

    # -------------------------------------------------------------------------
    # Velocity Amplitudes
    # -------------------------------------------------------------------------

    def V_r_i(
        self,
        n: int,
        r: float | Sequence,
    ) -> complex:
        """Radial incident field velocity term of mode `n`
        without Legendre coefficients

        Returns radial incident field velocity in [m/s]

        :param n: mode
        :param r: radial coordinate [m]
        """
        return self.field.A_in(n) * self.k_f * Bf.d1_besselj(n, self.k_f * r)

    def V_theta_i(
        self,
        n: int,
        r: float | Sequence,
    ) -> complex:
        """Tangential incident field velocity term of mode n
        without Legendre coefficients

        Returns tangential incident field velocity in [m/s]

        :param n: mode
        :param r: radial coordinate [m]
        """
        return self.field.A_in(n) * Bf.besselj(n, self.k_f * r) / r

    @abstractmethod
    def V_r_sc(
        self,
        n: int,
        r: float | Sequence,
    ) -> complex:
        """Radial scattering field velocity term of mode `n`
        without Legendre coefficients

        Returns radial scattering field velocity in [m/s]

        :param n: mode
        :param r: radial coordinate [m]
        """
        pass

    @abstractmethod
    def V_theta_sc(
        self,
        n: int,
        r: float | Sequence,
    ) -> complex:
        """Tangential scattering field velocity term of mode n
        without Legendre coefficients

        Returns tangential scattering field velocity in [m/s]

        :param n: mode
        :param r: radial coordinate [m]
        """
        pass

    def V_r(
        self,
        n: int,
        r: float,
        scattered: bool,
        incident: bool,
    ) -> complex:
        """Superposition of :meth:`~.V_r_sc()` and :meth:`~.V_r_i()` depending
        on :attr:`scattered` and :attr:`incident`

        At least one of the two must be `True`.

        :param n: mode
        :param r: radial coordinate [m]
        :param scattered: add scattered field
        :param incident: add incident
        """
        if scattered and incident:
            return self.V_r_i(n, r) + self.V_r_sc(n, r)
        elif scattered and not incident:
            return self.V_r_sc(n, r)
        elif not scattered and incident:
            return self.V_r_i(n, r)
        else:
            raise ValueError(
                "Neither scattered nor incident field has "
                "been has been selected. Velocity field is zero.",
            )

    def V_theta(
        self,
        n: int,
        r: float,
        scattered: bool,
        incident: bool,
    ) -> complex:
        """Superposition of :meth:`~.V_theta_sc()` and :meth:`~.V_theta_i()`
        depending on :attr:`scattered` and :attr:`incident`

        At least one of the two must be `True`.

        :param n: mode
        :param r: radial coordinate [m]
        :param scattered: add scattered field
        :param incident: add incident
        """
        if scattered and incident:
            if n == 0:
                return 0 * r
            return self.V_theta_i(n, r) + self.V_theta_sc(n, r)
        elif scattered and not incident:
            return self.V_theta_sc(n, r)
        elif not scattered and incident:
            return self.V_theta_i(n, r)
        else:
            raise ValueError(
                "Neither scattered nor incident field has "
                "been has been selected. Velocity field is zero.",
            )


class BaseScatteringRigidParticle(ABC):
    """Base class for the Scattering Field for a model with a rigid
    particle that defines the common interface.

    This base class is used for axisymmetric models.

    """

    # Required properties by child class

    R_0: float  # Angular frequency

    @abstractmethod
    def particle_velocity(self, t: float) -> complex:
        """Particle velocity

        Returns the value of the particle velocity
        in the direction of the axis of rotational
        symmetry of the radiation field in [m/s]

        :param t: time [s]
        """
        pass

    def radial_particle_velocity(
        self,
        r: float | Sequence,
        theta: float | Sequence,
        t: float | Sequence,
        mode: None | int = None,
    ) -> complex | NDArray:
        """Particle velocity in radial direction

        Returns the value of the particle velocity
        in radial direction in [m/s]

        :param r: radial coordinate [m]
        :param theta: tangential coordinate [rad]
        :param t: time [s]
        :param mode: specific mode number of interest; if `None` that all
                     modes until :attr:`.N_max`
        """
        if mode is None or mode == 1:
            r, theta, t = InputHandler.handle_input(
                r,
                theta,
                t,
                self.R_0,
                inside_sphere=True,
            )
            return self.particle_velocity(t) * cos(theta)
        else:
            return 0 * r * theta * t

    def tangential_particle_velocity(
        self,
        r: float | Sequence,
        theta: float | Sequence,
        t: float | Sequence,
        mode: None | int = None,
    ) -> complex | NDArray:
        """Particle velocity in tangential direction

        Returns the value of the particle velocity
        in tangential direction in [m/s]

        :param r: radial coordinate [m]
        :param theta: tangential coordinate [rad]
        :param t: time [s]
        :param mode: specific mode number of interest; if `None` that all
                     modes until :attr:`.N_max`
        """

        if mode is None or mode == 1:
            r, theta, t = InputHandler.handle_input(
                r,
                theta,
                t,
                self.R_0,
                inside_sphere=True,
            )
            return -self.particle_velocity(t) * sin(theta)
        else:
            return 0 * r * theta * t


if __name__ == "__main__":
    pass
