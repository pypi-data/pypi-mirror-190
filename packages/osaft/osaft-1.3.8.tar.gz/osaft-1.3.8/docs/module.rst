.. _Module:

OSAFT Module
===============

Solutions for the ARF
---------------------
.. toctree::
   :maxdepth: 1

   solutions/baseSolution
   solutions/baseARF
   solutions/baseScattering
   solutions/baseStreaming
   solutions/basedoinikov1994
   solutions/basedoinikov2021
   solutions/king1934
   solutions/yosioka1955
   solutions/hasegawa1969
   solutions/gorkov1962
   solutions/doinikov1994rigid
   solutions/doinikov1994compressible
   solutions/settnes2012
   solutions/doinikov2021viscous
   solutions/doinikov2021viscoelastic

.. _Plotting:

Plotting
--------
.. toctree::
   :maxdepth: 1

   plotting/scattering
   plotting/arf

.. _Core:

Core Modules
------------
.. toctree::
   :maxdepth: 2

.. currentmodule:: osaft.core

.. _Backgroundfields:

Backgroundfields
++++++++++++++++

.. autosummary::
   :toctree: generated/
   :template: template_class.rst
   :nosignatures:

    ~backgroundfields.BackgroundField


Materials
++++++++++

.. _Fluids:

Fluids
*******

.. inheritance-diagram:: fluids
   :top-classes: osaft.core.basecomposite.BaseFrequencyComposite
   :parts: 1

.. autosummary::
   :toctree: generated/
   :template: template_class.rst
   :nosignatures:

    ~fluids.InviscidFluid
    ~fluids.ViscousFluid
    ~fluids.ViscoelasticFluid

.. _Solids:

Solids
*******

.. inheritance-diagram:: solids
   :top-classes: osaft.core.basecomposite.BaseFrequencyComposite
   :parts: 1

.. autosummary::
   :toctree: generated/
   :template: template_class.rst
   :nosignatures:

    ~solids.RigidSolid
    ~solids.ElasticSolid

Composites
++++++++++

.. inheritance-diagram:: basecomposite
   :top-classes: frequency.Frequency geometries.Sphere
   :parts: 1

.. autosummary::
   :toctree: generated/
   :template: template_class.rst
   :nosignatures:

    ~frequency.Frequency
    ~geometries.Sphere
    ~basecomposite.BaseFrequencyComposite
    ~basecomposite.BaseSphereFrequencyComposite


Variable
++++++++

.. inheritance-diagram:: variable
   :top-classes: BaseVariable
   :parts: 1

.. autosummary::
   :toctree: generated/
   :template: template_class.rst
   :nosignatures:

    ~variable.BaseVariable
    ~variable.PassiveVariable
    ~variable.ActiveVariable

Helper
+++++++
.. autosummary::
   :toctree: generated/
   :template: template_class.rst
   :nosignatures:

   ~helper.StringFormatter
   ~helper.InputHandler


Functions
++++++++++
.. autosummary::
   :toctree: generated/
   :template: template_class.rst
   :nosignatures:

    ~functions.BesselFunctions
    ~functions.LegendreFunctions

.. autosummary::
   :toctree: generated/
   :nosignatures:

    ~functions.full_range
    ~functions.integrate
    ~functions.integrate_osc
    ~functions.spherical_2_cartesian_vector
    ~functions.cartesian_2_spherical_vector
    ~functions.cartesian_2_spherical_coordinates
    ~functions.spherical_2_cartesian_coordinates
    ~functions.clebsch_gordan_coefficient
    ~functions.xexpexp1

Enums, Exceptions, and Warnings
-------------------------------

Enums
+++++
.. autointenum:: osaft.core.backgroundfields.WaveType

Exceptions
++++++++++
.. autoexception:: osaft.core.backgroundfields.WrongWaveTypeError
   :exclude-members: with_traceback,args

Warnings
++++++++++
.. autoclass:: osaft.core.warnings.AssumptionWarning
   :exclude-members: with_traceback,args

.. autosummary::
   :toctree: generated/
   :nosignatures:

   osaft.core.warnings.raise_assumption_warning
