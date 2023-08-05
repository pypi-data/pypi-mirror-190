import unittest

from osaft import WaveType, doinikov1994rigid, settnes2012
from osaft.tests.basetest_arf import HelperCompareARF
from osaft.tests.basetest_numeric import BaseTestSolutions
from osaft.tests.solution_factory import SolutionFactory


class TestCompareSmallBoundaryLayer(BaseTestSolutions, HelperCompareARF):
    def setUp(self):
        super().setUp()

        self.arf_compare_threshold = 2e-1
        self.small_boundary_layer = True
        self.large_boundary_layer = False
        self.long_wavelength = True

        # Viscosity
        self.parameters._eta_f.high = 1e-3
        self.parameters._eta_f.low = 1e-5
        self.parameters.zeta_f = 0

        # Radius
        self.parameters._R_0.low = 10e-6
        self.parameters._R_0.high = 50e-6

        # Frequency
        self.parameters._f.low = 5e5
        self.parameters._f.high = 1e6

        # Density
        self.parameters._rho_f.low = 1500

        self.cls = SolutionFactory().doinikov_1994_rigid_arf()
        self.cls.long_wavelength = self.long_wavelength
        self.cls.large_boundary_layer = self.large_boundary_layer
        self.cls.small_boundary_layer = self.small_boundary_layer

        self.compare_cls = SolutionFactory().doinikov_1994_rigid_arf()
        self.compare_cls.long_wavelength = self.long_wavelength
        self.list_cls = [self.cls, self.compare_cls]
        self.assign_parameters()


class TestCompareSmallParticleGeneral(BaseTestSolutions):
    def setUp(self):
        super().setUp()

        self.arf_compare_threshold = 1e-1

        self.parameters._R_0.low = 1e-6
        self.parameters._R_0.high = 5e-6
        self.parameters._eta_f.low = 1e-6
        self.parameters._eta_f.high = 1e-3
        self.parameters._f.high = 5e5

        self.large_boundary_layer = False
        self.small_boundary_layer = False

        self.cls = doinikov1994rigid.ARF(
            self.f,
            self.R_0,
            self.rho_s,
            self.rho_f,
            self.c_f,
            self.eta_f,
            self.zeta_f,
            self.p_0,
            WaveType.STANDING,
            self.position,
            long_wavelength=True,
        )

        self.compare_cls = doinikov1994rigid.ARF(
            self.f,
            self.R_0,
            self.rho_s,
            self.rho_f,
            self.c_f,
            self.eta_f,
            self.zeta_f,
            self.p_0,
            WaveType.STANDING,
            self.position,
            long_wavelength=False,
        )

        self.list_cls = [self.cls, self.compare_cls]

    def test_with_background_streaming(self):
        self.cls.background_streaming = True
        self.compare_cls.background_streaming = True
        self.do_testing(
            self.cls.compute_arf,
            self.compare_cls.compute_arf,
            threshold=self.arf_compare_threshold,
            zero=1e-30,
        )

    def test_without_background_streaming(self):
        self.cls.background_streaming = False
        self.compare_cls.background_streaming = False
        self.parameters._wave_type.list_of_values = [WaveType.STANDING]
        self.do_testing(
            self.cls.compute_arf,
            self.compare_cls.compute_arf,
            threshold=self.arf_compare_threshold,
            zero=1e-30,
        )


class TestCompareSettnes(BaseTestSolutions, HelperCompareARF):
    def setUp(self):
        super().setUp()

        self.arf_compare_threshold = 10e-2
        self.small_boundary_layer = False
        self.large_boundary_layer = False
        self.long_wavelength = True

        # Viscosity
        self.parameters._eta_f.high = 1e-3
        self.parameters._eta_f.low = 1e-5
        self.parameters._eta_f.value = 1e-4
        self.parameters.zeta_f = 0

        # Radius
        self.parameters._R_0.low = 1e-6
        self.parameters._R_0.high = 10e-6

        # Frequency
        self.parameters._f.low = 1e6
        self.parameters._f.high = 2e6

        # Density
        self.parameters._rho_s.low = 1500
        self.parameters._rho_s.high = 2000

        # Speed of Sound Scatterer
        self.parameters._c_s.low = 1e6
        self.parameters._c_s.high = 1e6

        # Wave Type
        self.parameters._wave_type.list_of_values = [WaveType.STANDING]
        self.parameters.wave_type = WaveType.STANDING

        self.cls = doinikov1994rigid.ARF(
            self.f,
            self.R_0,
            self.rho_s,
            self.rho_f,
            self.c_f,
            self.eta_f,
            self.zeta_f,
            self.p_0,
            self.wave_type,
            self.position,
            long_wavelength=self.long_wavelength,
            large_boundary_layer=self.large_boundary_layer,
            small_boundary_layer=self.small_boundary_layer,
            background_streaming=False,
        )

        self.compare_cls = settnes2012.ARF(
            self.f,
            self.R_0,
            self.rho_s,
            self.c_s,
            self.rho_f,
            self.c_f,
            self.eta_f,
            self.p_0,
            self.wave_type,
            self.position,
        )

        self.list_cls = [self.cls, self.compare_cls]


if __name__ == "__main__":
    unittest.main()
