import unittest

from osaft.core.functions import pi, sin
from osaft.tests.basetest_arf import (
    HelperCompareARF,
    HelperStandingARF,
    HelperTravelingARF,
)
from osaft.tests.basetest_numeric import BaseTestSolutions
from osaft.tests.solution_factory import SolutionFactory


class TestGorkov(BaseTestSolutions):
    def setUp(self) -> None:
        super().setUp()

        self.cls = SolutionFactory().gorkov_1962_arf()
        self.list_cls = [self.cls]

    # -------------------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------------------

    @property
    def f_1(self):
        return 1 - self.cls.kappa_s / self.cls.kappa_f

    @property
    def f_2(self):
        rho_tilde = self.rho_s / self.rho_f
        return 2 * (rho_tilde - 1) / (2 * rho_tilde + 1)

    @property
    def Phi(self):
        return self.f_1 / 3 + self.f_2 / 2

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    def test_properties(self) -> None:
        properties = ["f_1", "f_2", "Phi"]
        self._test_properties(properties)

    def test_not_small_particle(self):
        # This method is not actually testing, only for coverage
        self.cls.R_0 = self.cls.fluid.lambda_f
        self.cls.compute_arf()


class TestStandingARF(TestGorkov, HelperStandingARF):
    def compute_arf(self):
        out = 4 * pi * self.cls.Phi * self.cls.k_f * self.R_0**3
        out *= self.cls.E_ac * sin(2 * self.position)
        return out


class TestTraveling(TestGorkov, HelperTravelingARF):
    def compute_arf(self):
        A = self.p_0 / (1j * 2 * pi * self.f * self.rho_f)
        out = 2 / 9 * pi * self.rho_f * abs(A) ** 2
        out *= (self.cls.k_f * self.R_0) ** 6
        out *= self.f_1**2 + self.f_1 * self.f_2 + 3 / 4 * self.f_2**2
        return out


class TestCompareToKing(TestGorkov, HelperCompareARF):
    def setUp(self) -> None:

        super().setUp()

        self.parameters.R_0 = 1e-7
        self.parameters._R_0.high = 1e-6

        self.parameters.c_s = 1e10
        self.parameters._c_s.low = 1e9

        self.arf_compare_threshold = 1e-4

        self.cls = SolutionFactory().gorkov_1962_arf()
        self.compare_cls = SolutionFactory().king_1934_arf()
        self.compare_cls.small_particle_limit = True

        self.list_cls = [self.cls, self.compare_cls]


if __name__ == "__main__":
    unittest.main()
