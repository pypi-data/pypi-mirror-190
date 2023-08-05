from osaft.core.functions import BesselFunctions as Bf
from osaft.tests.basetest_numeric import BaseTestSolutions
from osaft.tests.solution_factory import SolutionFactory


class BaseKing(BaseTestSolutions):
    def setUp(self) -> None:

        super().setUp()

        self.cls = SolutionFactory().king_1934_base()
        self.list_cls = [self.cls]

    # -------------------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------------------

    @staticmethod
    def phi_n(n: int, arg):
        return -1 / arg**n * Bf.bessely(n, arg)

    @staticmethod
    def psi_n(n: int, arg):
        return 1 / arg**n * Bf.besselj(n, arg)

    def F_n(self, n: int, arg):
        if n == 1:
            out = self.cls.alpha**2 * self.phi_n(n + 1, arg)
            out -= (1 - 1 / self.cls.rho_tilde) * self.phi_n(n, arg)
        else:
            out = self.cls.alpha**2 * self.phi_n(n + 1, arg)
            out -= n * self.phi_n(n, arg)

        return out

    def G_n(self, n: int, arg):
        if n == 1:
            out = self.cls.alpha**2 * self.psi_n(n + 1, arg)
            out -= (1 - 1 / self.cls.rho_tilde) * self.psi_n(n, arg)
        else:
            out = self.cls.alpha**2 * self.psi_n(n + 1, arg)
            out -= n * self.psi_n(n, arg)

        return out

    @property
    def rho_tilde(self):
        return self.cls.rho_s / self.rho_f

    @property
    def alpha(self):
        return self.cls.R_0 * self.cls.k_f

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    def test_properties(self) -> None:
        properties = ["alpha", "rho_tilde"]
        self._test_properties(properties)
