# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

In the section [Unreleased](#unreleased) all changes are gathered that will be
packed into the next release. A new release must be initialized via a new merge
request.

## Unreleased
### Fixed (_ changes)
### Added (_ changes)
### Changed (_ changes)
### Removed (_ changes)

## 1.3.8 (2023-02-06)
### Changed (1 change)
- moved project configuration to `pyproject.toml`

## 1.3.7 (2022-11-18)
### Fixed (1 change)
- naming of frequency and radius in `installation.rst` @apavlic
### Added (5 changes)
- quiver plots for acoustic fluid velocity plots/animation @ExtremOPS
- New grid classes by @jonas.fankhauser
- example showcasing quiver plot capabilities @ExtremOPS
- `SolutionFactory` to generate solutions for testing added by @jonas.fankhauser
- `black` as code formatter @ExtremOPS
### Changed (7 changes)
- use `pytest` instead of `unittest discover` @ExtremOPS
- `pytest` configuration put into `tox.ini` and `.coveragerc` @ExtremOPS
- fixed imports for usage of `pytest` @ExtremOPS
- python:buster-3.11 as default CI/CD image @ExtremOPS
- separate solutions folder under `osaft/tests/...` @ExtremOPS
- `sphinx-build` uses all available cores @ExtremOPS
- Test for scattering plots changed, tests for all models added by @jonas.fankhauser
### Removed (2 changes)
- `create_changelog.py` and all auxillieries @ExtremOPS
- timing in `BaseTest` @ExtremOPS

## 1.3.6 (2022-10-25)
### Added (1 change)
- Python 3.11 support @ExtremOPS
### Changed (1 change)
- docu is build as soon as 3.11 testing (fastest) is passed @ExtremOPS

## 1.3.5 (2022-10-20)
### Added (2 changes)
- testing for print statements in pre-commit hooks @ExtremOPS
- flake8-print in requirements_dev.txt @ExtremOPS
### Changed (1 change)
- upload coverage.xml file for Gitlab test analysis @ExtremOPS

## 1.3.4 (2022-10-11)
### Added (1 change)
- added examples from presentation from AF2022 by @jonas.fankhauser
### Changed (1 change)
- small changes to the index page by @jonas.fankhauser

## 1.3.3 (2022-09-02)
### Fixed (1 change)
- Update to make osaft run with Matplotlib >= 3.6 by @jonas.fankhauser

## 1.3.2 (2022-09-02)
### Changed (1 change)
- overwrites default kwargs if set by user by @ExtremOPS

## 1.3.1 (2022-08-31)
### Added (1 change)
- added scattering field from Doinikov 2021 (viscoelastic fluid, elastic sphere) by @jonas.fankhauser

## 1.3.0 (2022-08-25)
### Added (2 changes)
- added model from Doinikov 2021 (viscous fluid, elastic sphere) by @jonas.fankhauser
- example Doinikov (2021), convergence study by @jonas.fankhauser

## 1.2.2 (2022-08-31)
### Added (2 changes)
- `custom.js` for external links in new tab @ExtremOPS
- `AssumptionWarning` @ExtremOPS
### Changed (2 changes)
- all `compute_arf()` methods to check for assumptions and raise AssumptionWarning @ExtremOPS
- parallel execution of test stages in CI
### Fixed (1 change)
- table in `examples/tutorial/example_doinikov_1994.py` @ExtremOPS

## 1.2.1 (2022-08-29)
### Added (1 change)
- Automatically changing `N_max` during testing @jonas.fankhauser

## 1.2.0 (2022-08-24)
### Added (5 changes)
- general solution for Doinikov 1994 Rigid Particle by @jonas.fankhauser
- general solution for Doinikov 1994 Compressible Particle by @jonas.fankhauser
- example possible numerical issues by @jonas.fankhauser
- example Doinikov 1994 models by @jonas.fankhauser
- example pressure plots by @ExtremOPS
### Changes (1 change)
- osaft library requires mpmath > 1.2.0

## 1.1.3 (2022-08-17)
### Fixed (1 change)
- mistake in Settnes & Bruus fixed according to Marston (2013) by @jonas.fankhauser

## 1.1.2 (2022-08-10)
### Fixed (1 change)
- data visualisation in tricontourf animation of pos/neg data @ExtremOPS
### Added (5 changes)
- abstract potential_coefficient(n: int) in BaseScattering @ExtremOPS
- velocity_potential(...) and pressure(...) to BaseScattering @ExtremOPS
- velocity_potential and pressure plot in FluidScatteringPlot @ExtremOPS
- diverging colormap in FluidScatteringPlot @ExtremOPS
- attributes (set/get) for both colormaps in FluidScatteringPlot @ExtremOPS
### Changed (2 changes)
- animations buttons black text on white bg @ExtremOPS
- rounded corners for all images @ExtremOPS

## 1.1.1 (2022-08-03)
### Added (1 change)
- logo with transparent bg + *.psd file @ExtremOPS
### Changed (2 changes)
- moved examples to subfolders @ExtremOPS
- added version restriction to sphinx-gallery @ExtremOPS
### Removed (1 change)
- spicific logos for light/dark theme @ExtremOPS

## 1.1.0 (2022-08-03)
### Added (1 change)
- added the model by Hasegawa & Yosioka (1969) and Hasegawa (1979) by @merrillg

## 1.0.7 (2022-08-03)
### Added (1 change)
- functions for converging elastic constant by @jonas.fankhauser

## 1.0.6 (2022-08-02)
### Added (1 change)
- multiprocessing support added for `ARFPlot` by @jonas.fankhauser

## 1.0.5 (2022-07-20)
### Changed (3 changes)
- renamed SpecialFunctions to BesselFunctions by @jonas.fankhauser
- integrate returns value and error estimate by @jonas.fankhauser
- V_theta(n) set automatically to 0 for n == 0 by @jonas.fankhauser
### Added (1 change)
- PyPi page updated (link to paper, framework -> library) by @jonas.fankhauser
### Fixed (3 changes)
- corrected type for wave_type wrapper methods by @jonas.fankhauser
- return type for `wave_type` wrapper methods by @jonas.fankhauser
- many typos and mistakes in documentation corrected by @jonas.fankhauser

## 1.0.4 (2022-07-19)
### Fixed (1 change)
- fixing the comparison of a complex and a real number by @jonas.fankhauser

## 1.0.3 (2022-06-30)
### Fixed (1 change)
- going back to released version of `sphinx_gallery` @jonas.fankhauser

## 1.0.2 (2022-06-24)
### Changed (2 changes)
- added new normalization methods for ARF plot @jonas.fankhauser
- added new `display_values` parameter for ARF plot by @jonas.fankhauser

## 1.0.1 (2022-06-21)
### Changed (1 change)
- renamed sphere area and volume to make it less confusing by @jonas.fankhauser
### Fixed (1 change)
- fixed verify_changelog.py @jonas.fankhauser

## 1.0.0 (2022-06-20)
### Added (2 changes)
- bibtex and link to publications by @ExtremOPS
- python 3.10 version support in setup.py @ExtremOPS
### Changed (2 changes)
- python 3.9 tested first @ExtremOPS
- badges to README @ExtremOPS

## 0.9.17 (2022-06-20)
### Added (1 change)
- explicit sphinx version >= 5.0 by @ExtremOPS
### Fixed (1 change)
- adapted EnumDocumenter to Sphinx >= 5.0 by @ExtremOPS

## 0.9.16 (2022-05-31)
### Changed (2 changes)
- sphinx-gallery requirement points to SHA by @ExtremOPS
- exclude linenumbers for copybutton by @ExtremOPS
### Added (2 changes)
- white background for inheritance diagram in css by @ExtremOPS
- refernce_url in docs for cross-linking by @ExtremOPS
### Fixed (1 change)
- identation levels of docstrings by @ExtremOPS

## 0.9.15 (2022-04-19)
### Changed (2 changes)
- usage of BaseSolution.copy() in examples by @ExtremOPS
- frequency -> f; radius -> R_0 by @ExtremOPS
### Added (1 change)
- copy method for BaseSolution by @ExtremOPS

## 0.9.14 (2022-04-19)
### Added (4 changes)
- Support for Python 3.10 by @jonas.fankhauser
- Examples from publications added by @ExtremOPS
- new methods `input_variables()` for solution classes by @jonas.fankhauser
- new max-norm for normalized ARF plot by @jonas.fankhauser
### Changed (3 changes)
- package names of solutions (e.g. `gorkov1962`) no longer capitalized by @jonas.fankhauser
- `add_solution()` -> `add_solutions()` by @jonas.fankhauser
- more detailed explanations in all examples by @jonas.fankhauser
### Fixed (3 changes)
- Links in README (builder: html) by @ExtremOPS
- Correct linestyles in examples in documentation website by @jonas.fankhauser
- Typing fixed for Python 3.10 support

## 0.9.13 (2022-04-13)
### Fixed (1 change)
- create_changelog.py pulls the newest changes to CHANGELOG.md first by @ExtremOPS

## 0.9.12 (2022-03-31)
### Fixed (1 change)
- fixed documentation in `base_scattering` by @jonas.fankhauser

## 0.9.11 (2022-03-25)
### Added (3 changes)
- Python version in installation description by @jonas.fankhauser
- Fixed versions in `requirement.txt` by @jonas.fankhauser
- PS particle example by @jonas.fankhauser

## 0.9.10 (2022-03-21)
### Added (4 changes)
- New base solution for `Doinikov1994Rigid`, `Doinikov1994Compressible` by @jonas.fankhauser
- Use ActiveListVariable in `Doinikov1994Compressible` solution added by @jonas.fankhauser
- `__repr__` for `Doinikov1994Compressible` by @jonas.fankhauser
- `__str__` for `Doinikov1994Rigid` by @jonas.fankhauser

## 0.9.9 (2022-03-21)
### Changed (1 change)
- simplified coefficient matrix in `BaseDoinikov1994Compressible` by @jonas.fankhauser

## 0.9.8 (2022-03-21)
### Changed (1 change)
- added regex to match protected release tags by @ExtremOPS

## 0.9.7 (2022-03-16)
### Added (2 changes)
- new ActiveListVariable class by @jonas.fankhauser
- usage of observer pattern extended in King1934 by @jonas.fankhauser
### Fixed (2 changes)
- Bug fix, position, wave_type mixed up by @jonas.fankhauser

## 0.9.6 (2022-03-16)
### Changed (2 changes)
- unified checking of supported `wave_type` in `BaseSolution` by @jonas.fankhauser
- `WaveTypes` -> `WaveType` by @jonas.fankhauser

## 0.9.5 (2022-03-08)
### Changed (1 change)
- fixed readthedocs homepage by @jonas.fankhauser

## 0.9.4 (2022-03-07)
### Changed (1 change)
- acoustic_radiation_force() -> compute_arf() by @ExtremOPS

## 0.9.3 (2022-03-07)
### Changed (3 changes)
- 'Default' highlighted with color by @ExtremOPS
- html theme -> Furo w/ light and dark logo by @ExtremOPS
- InputTest simplified by @jonas.fankhauser
### Added (3 changes)
- Excluding dunders in 'Public Methods' section by @ExtremOPS
- missing Docstrings by @ExtremOPS
- ico file for browers by @ExtremOPS

## 0.9.2 (2022-03-04)
### Changed (1 change)
- pointing to stable version (main) by @ExtremOPS

## 0.9.1 (2022-03-03)
### Added (1 change)
- deployment pipeline for PyPi by @jonas.fankhauser

## 0.9.0 (2022-03-03)
### Changed (many changes)
- renamed `gorkov` to `osaft` @ExtremOPS
- coverage within testing stage @ExtremOPS

## 0.8.3  (2022-03-03)
### Changed (1 change)
- Doinikov 1994 (compressible) with same interface as Doinikov 1994 (rigid) by @jonas.fankhauser

## 0.8.2  (2022-02-28)
### Changed (1 change)
- documentation improved and examples added by @jonas.fankhauser
- examples shown in Sphinx gallery by @ExtremOPS

## 0.8.1 (2022-02-28)
### Changed (1 change)
- fixed order of CHANGELOG by @ExtremOPS
### Removed (1 change)
- in pre-commit stage 'pip install .'  @ExtremOPS
### Added (1 change)
- check_changelog_order.py for CI by @ExtremOPS

## 0.8.0  (2022-02-28)
### Added (1 change)
- limiting cases for Doinikov 1994 compressible particle implemented by @ExtremOPS

## 0.7.0  (2022-02-25)
### Added (2 changes)
- plotting functionality for the scattering field by @jonas.fankhauser
- plotting functionality for the ARF by @ExtremOPS

## 0.6.14 (2022-02-17)
### Fixed (1 change)
- Fix for `physical_position` by @jonas.fankhauser
### Changed (2 changes)
- Moved `physical_position` to core.backgroundfields by @jonas.fankhauser
- Moved `physical_position` to `abs_pos` by @jonas.fankhauser

## 0.6.13 (2022-02-17)
### Fixed (1 change)
- test_name_attribute only for instances of `BaseSolution` by @jonas.fankhauser

## 0.6.12 (2022-02-16)
### Changed (1 change)
- Position is in units of rad instead of fixed in space by @ExtremOPS

## 0.6.11 (2022-02-10)
### Changed (1 change)
- fixed get_version in setup.py by @ExtremOPS
- 'src' -> 'gorkov' @ExtremOPS

## 0.6.10 (2022-02-08)
### Added (1 change)
- isort pre-commit hook by @jonas.fankhauser
### Changed (4 changes)
- renamed `src` -> `gorkov`
- moved `tests` -> `gorkov/tests`
- reorganized imports everywhere @jonas.fankhauser
- change top level `__init__.py` file @jonas.fankhauser
### Removed (1 change)
- removed `gorkov/core/types.py` @jonas.fankhauser

## 0.6.9 (2022-01-31)
### Added (1 change)
- Doinikov1994Rigid added solution for arbitrary BL thickness by @jonas.fankhauser

## 0.6.8 (2022-01-27)
### Changed (2 changes)
- changed the name `solid` to `scatterer`where it describes the
  particle/droplet/bubble by @fjonas
- various cosmetic changes by @fjonas

## 0.6.7 (2022-01-24)
### Added (1 change)
- new function xexpexp1 implemented by @fjonas

## 0.6.6 (2022-01-19)
### Fixed (1 change)
- scipy spherical Bessel functions instead of own definition by @fjonas

## 0.6.5 (2022-01-17)
### Added (1 change)
- needs_update property to ActiveVariable by @ExtremOPS

## 0.6.4 (2022-01-17)
### Added (1 change)
- particle displacement methods added by @fjonas

## 0.6.3 (2021-12-28)
### Changed (1 change)
- PassiveVariable can also be list/np.ndarray/etc. by @ExtremOPS

## 0.6.2 (2021-12-09)
### Changed (1 change)
- V_r and V_theta in BaseScattering are now computed in separate methods by
  @fjonas

## 0.6.1 (2021-12-03)
### Changed (1 change)
- test in King reorganised by @fjonas

## 0.6.0 (2021-12-02)
### Added (1 change)
 - solution for the scattering field and limiting cases of the acoustic
   radiation force from Doinikov 1994 viscous fluid and rigid particle added by
   @ExtremOPS

## 0.5.2 (2021-12-02)
### Changed (2 changes)
- folder gorkov --> src by @ExtremOPS
- branch testing in coverage run @ExtremOPS
### Removed (1 change)
- redundant elif clauses @ExtremOPS

## 0.5.1 (2021-12-01)
### Added (1 change)
- zero argument added to to BaseTest.do_testing by @fjonas

## 0.5.0 (2021-11-30)
### Added (1 change)
 - solution from Yosioka & Kawasima added by @mastc and @fjonas

## 0.4.38 (2021-11-29)
### Added (6 changes)
- unittest tangential_particle_velocity by @goeringc
- unittest radial_particle_velocity by @goeringc
- unittest tangential_mode_superposition by @goeringc
- unittest radial_mode_superposition by @goeringc
- unittest V_theta_i by @goeringc
- unittest for V_r_i by @goeringc

## 0.4.37 (2021-11-29)
### Changed (1 change)
- used new generic methods for testing properties and func(n, ...) by @goeringc
### Added (2 changes)
- generic method to test methods where the first argument is n by @goeringc
- generic method for testing properties by @goeringc
### Removed (1 change)
- whitespace between @ \w by @goeringc

## 0.4.36 (2021-11-26)
### Changed (1 change)
- string formating for SubTest in HelperCompareScattering by @fjonas

## 0.4.35 (2021-11-25)
### Added (3 changes)
- particle velocity comparison by @goeringc
- threshold for boundary conditions testing by @goeringc
- Compare algorithm for two scattering solutions by @goeringc

## 0.4.34 (2021-11-25)
### Changed (5 changes)
- no capitals in filenames by @goeringc
- filenames without capital letters in tests and solutions by @goeringc
- removed redundant information in test files/classes for Gorkov by @goeringc
- removed redundant information in test files/classes for Settnes by @goeringc
- removed redundant information in test files/classes for King by @goeringc

## 0.4.33 (2021-11-25)
### Changed (1 change)
- order of calls to show recomputed value in log by @goeringc

## 0.4.32 (2021-11-25)
### Changed (3 changes)
- testing of complex valued velocities by @fjonas
- tests for King adapted to new style by @fjonas
- base_scattering.py reorganized by @fjonas
### Added (1 change)
- mode testing added for radial/tangential_particle_velocities by @fjonas

## 0.4.31 (2021-11-19)
### Added (2 changes)
- default name to King, Gorkov, Settnes by @goeringc
- BaseSolution with name attribute and unittests in BaseTest by @goeringc

## 0.4.30 (2021-11-18)
### Changed (1 change)
- moved common methods to `HelperScattering` by @fjonas

## 0.4.29 (2021-11-18)
### Added (2 changes)
- BaseScatteringRigidParticle added by @fjonas
- InputeHandle added for r, theta, and t by @fjonas

## 0.4.28 (2021-11-18)
### Changed (1 change)
- Moved Incident fluid velocity in baseclass by @goeringc

## 0.4.27 (2021-11-17)
### Changed (1 change)
- Usage of WrongWaveTypeError by @goeringc
### Added (1 change)
- Enum for WaveTypes by @goeringc
### Removed (1 change)
- str option of StringFormatter by @goeringc

## 0.4.26 (2021-11-16)
### Added (1 change)
- coordinate and velocity transformation function completed by @fjonas
### Fixed (1 change)
- `AssertAlmostEqual` uses input argument `threshold` also for zero comparison by @fjonas

## 0.4.25 (2021-11-09)
### Added (2 changes)
- precommit pep858 upgrade and its changes to files by @goeringc
- add-trailing-commas precommit plus changes through it by @goeringc

## 0.4.24 (2021-11-05)
### Changed (1 change)
- nbr_runs -> n_runs by @goeringc
### Added (3 changes)
- list_of_values property for ChangingFromList by @goeringc
- property and test n_runs >=! ChaingingFromList.longest_list by @goeringc
- ChangingFromList is cycling through all posibilities by @goeringc

## 0.4.23 (2021-11-05)
### Changed (3 changes)
- test_variables is set instead of tuple by @goeringc
- renamed formatter module to helper by @goeringc
- restrict theta to be smaller than pi by @goeringc
### Added (5 changes)
- RadiusTester in King, BaseScattering, and Tests by @goeringc
- RadiusTester for inside/outside of sphere and unittests by @goeringc
- ThetaTester to fluid and particle velocity for King and in BaseScattering by @goeringc
- Test in HelperScattering to see if right theta values are enforced by @goeringc
- ThetaTester class and tests to it by @goeringc
### Fixed (1 change)
- order of arguments by @goeringc

## 0.4.22 (2021-11-04)
### Changed (2 changes)
- do_testing used for test A_in in backgroundfields.py by @fjonas
- imports reoganized in all files by @fjonas
### Fixed (2 changes)
- typos corrected other cosmetic changes by @fjonas
- wrong use of type hint Optional corrected in all files by @fjonas

## 0.4.21 (2021-11-04)
### Changed (3 changes)
- wave_type in Gorkov1962 has no default argument by @fjonas
- order of arguments to init for classes in King1934 adapted by @fjonas
- order of arguments to init for classes in Settnes2012 adapted by @fjonas
-
## 0.4.20 (2021-11-04)
### Changed (1 change)
- Return complex-valued velocities by @goeringc
### Fixed (2 changes)
- Right sign for particle velocity by @goeringc
- testing of scattering BCs by @goeringc

## 0.4.19 (2021-11-03)
### Added (1 change)
- wave_typ in tests is now of type ChangingFromList by @fjonas
### Changed (4 changes)
- Tests King1932, Gorkov1962, Settnes2012 adapted to new style by @fjonas
- Tests for acoustic intensity adapted by @fjonas
- HelperStandingARF, HelperTravelingARF adapted by @fjonas
- Gor'kov comparison with King uses HelperCompareARF @fjonas
### Fixed (1 change)
- Wrong inheritances in King1932.ARF fixed by @fjonas
### Removed (1 change)
- Redundant standing/traveling wave tests removed by @fjonas

## 0.4.18 (2021-11-03)
### Fixed (2 changes)
- Missing link to wave_type in variable Phi in King by @fjonas
- Missing link to rho_tilde in variable Phi in King by @fjonas

## 0.4.17 (2021-11-02)
### Added (2 changes)
- Missing tests for arf.py in King, Gorkov, & Settnes for 100% coverage by @fjonas
- Missing test for integrate_osc in functions.py by @fjonas

## 0.4.16 (2021-11-02)
### Changed (1 change)
- regex pattern for getting latest version by @goeringc
### Added (1 change)
- try block if token JSON file is there by @goeringc

## 0.4.15 (2021-11-02)
### Changed (1 change)
- Changed style of version and date in CHANGELOG.md by @goeringc
### Added (1 change)
- create_changelog.py for automatic log entries by @goeringc

## 0.4.14 (2021-11-02)
### Changed/Added - Jonas Fankhauser
 - ChangingBool added
 - bugfix in ChangingInt
 - new getters and setters for low and high in ChangingNumber
 - tests for all child classes of BaseChangingVariable

## 0.4.13 (2021-11-01)
### Changed/Added - Jonas Fankhauser
 - signature of do_testing has been changed to be more readable
 - redundant test methods have been removed
 - SubTest context manager added to do_testing
 - BaseChangingVariable introduced for testing

## 0.4.12 (2021-10-27)
### Bugfix - Jonas Fankhauser
 - bugfix in first_cos_poly

## 0.4.11 (2021-10-25)
### Added - Christoph Goering
 - automated testing of boundary condition in scattering field

## 0.4.10 (2021-10-25)
### Added - Jonas Fankhauser
 - added missing wrappers for setters and getters in BackgroundField

## 0.4.9 (2021-10-21)
### Changed - Christoph Goering
 - moved V_r_i, V_r_sc, V_theta_i, V_theta_sc as @abstractmethod into BaseStreaming
 - moved attribute N_max into BaseScattering
 - removed @abstractmethod from tangential_acoustic_fluid_velocity and tangential_acoustic_fluid_velocity in BaseStreaming
 - added test script for BaseStreaming
 - removed N_max from King1932.ScatteringField
 - removed small_particle_limit from BaseKing and put into King1932.ARF
 - added mode input for particle velocities in King1932.ScatteringField

## 0.4.8 (2021-10-15)
### Added - Christoph Goering
 - added BaseTestCompareARF standardized comparing of different ARF solutions

## 0.4.7 (2021-10-14)
### Added - Christoph Goering
 - property to Backgroundfield for the squared absolute amplitude A

## 0.4.6 (2021-11-07)
### Added - Jonas Fankhauser
 - function integrate_osc added to function.py

## 0.4.5 (2021-10-07)
### Changed - Jonas Fankhauser, Christoph Goering
 - type hints removed from docstring
 - removed `:return:`  statements form docstrings

## 0.4.4 (2021-10-07)
### Added - Christoph Goering
 - padding around inheritance diagrams

## 0.4.3 (2021-10-07)
### Changed - Christoph Goering
 - BaseTest: one function to retrieve value from parameters that are a Callalble and a Tuple of arguments
 - relative difference in testing is absolute
 - BaseTestScattering has attributes for the particle and fluid velocity to change it per model
 - BaseTestScattering rename `self.scattering` to `self.cls`
 - adapted new changes to `test_KingScattering.py`

## 0.4.2 (2021-10-04)
### Added - Christoph Goering
 - missing tests for King (particle velocity)

## 0.4.1 (2021-10-04)
### Changed - Christoph Goering
 - derived BaseTest____ class needs to call BaseTest____._assign_parameters()
 - zeta_F --> zeta_f in BaseTestViscousFluid

## 0.4.0 (2021-09-23)
### Added - David Ruckstuhl and Christoph Goering
 - Scattering and ARF for King's Theory of 1934
 - BaseTestARF, BaseTestTravellingARF, BaseTestStandingARF
 - BaseTestInviscidFluid, BaseTestViscousFluid, BaseTestRigidSolid
### Changed - Christoph Goering
 - unittest structure; each model has its own folder as in the module
 - adapted current module to new BaseTest classes

## 0.3.4 (2021-08-23)
### Changed - Christoph Goering
- fixed links to other :attr:, :func:, :classes: in documentation
- added :math: and unit to missing @properties

## 0.3.3 (2021-08-24)
### Added - Christoph Goering
- missing tests for backgroundfield

## 0.3.2 (2021-08-23)
### Changed - Christoph Goering
- fixed bug that difference could be negative and then it is always smaller
  than the threshold

## 0.3.1 (2021-08-19)
### Added - Christoph Goering
- do_testing() in BaseTest to reduce redundant lines of code
- list of independent variable names for single variable change

## 0.3.0 (2021-08-19)
### Added - Jonas Fankhauser
 - ARF model from Settnes and Bruus for a viscous fluid

## 0.2.19 (2021-08-19)
### Changed - Jonas Fankhauser
 - inviscid case for viscous and viscoelastic fluids

## 0.2.18 (2021-08-17)
### Changed - Jonas Fankhauser
 - linking of variables is tested by changing every variable individually

## 0.2.17 (2021-06-08)
### Changed - Jonas Fankhauser
 - bugfix for ViscoElasticFluid class

## 0.2.16 (2021-05-20)
### Changed - Jonas Fankhauser
 - removed Doinikov2021 specific methods from fluid classes

## 0.2.15 (2021-05-03)
### Changed - Jonas Fankhauser
 - cosmetic: corrected errors and typos in the docstrings

## 0.2.14 (2021-04-27)
### Changed - Christoph Goering
 - fixed possible type in formatter to include None

## 0.2.13 (2021-04-21)
### Added - Christoph Goering
 - timing in basetest class
### Changed - Christoph Goering
 - fixed import in testing for 'python setup.py test'
 - verbose output for unittests
 - fixed error in `test_for_changelog.sh`

## 0.2.12 (2021-04-20)
### Added - Christoph Goering
 - CI checks also for changes in CHANGELOG.md

## 0.2.11 (2021-04-20)
### Changed - Jonas Fankhauser
 - Used acoustic energy and intensity in Gor'kov solution

## 0.2.10 (2021-04-20)
### Changed - Jonas Fankhauser
 - Bug fix for 0.2.8

## 0.2.9 (2021-04-15)
### Changed - Christoph Goering
 - unified position of units in doc string

## 0.2.8 (2021-04-13)
### Added - Cyrill Mast
 - Acoustic Energy
 - Acoustic Intensity

## 0.2.7 (2021-03-29)
### Changed - Cyrill Mast
 - A_in was not dependent on the wavetype and was therefore not updated correctly

## 0.2.6 (2021-03-01)
### Added - Cyrill Mast
 - Spherical Hankel function of the second kind
### Changed
 - changed names of special functions
 - updated tests for special funcitons

## 0.2.5 (2021-03-01)
### Added - Cyrill Mast
 - Spherical Neumann Functions

## 0.2.4 (2021-02-25)
### Changed - Jonas Fankhauser
 - BaseStreaming for Eulerian and Langerian fields

## 0.2.3 (2021-02-19)
### Added - Jonas Fankhauser
 - BaseStreaming for all future streaming fields
 - BaseScattering for all future scatterings fields
### Changed - Jonas Fankhauser
 - BaseVariable has name attribute for logging and debugging

## 0.2.2 (2021-02-13)
### Changed - Christoph Goering
 - refactoring of module structure
 - all imports to new structure

## 0.2.1 (2021-02-13)
### Added - Christoph Goering
 - all missing unittests

## 0.2.0 (2021-02-04)
### Added - Christoph Goering
 - Small Particle Limit ARF for King's Theory of 1932

## 0.1.1 (2021-02-05)
### Changed - Christoph Goering
 - Single site documentation

## 0.1.0 (2021-02-04)
### Added - Christoph Goering
 - ARF for Gor'kov's Theory of 1964
 - BaseARF for all future ARF solutions
