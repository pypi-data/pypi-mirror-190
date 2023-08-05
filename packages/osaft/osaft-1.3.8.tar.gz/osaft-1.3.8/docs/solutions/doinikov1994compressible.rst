.. _Doinikov1994Compressible:

Doinikov (viscous fluid - compressible sphere; 1994)
====================================================

We have implemented a modified version of the following paper.Doinikov
covers in this publication also the case of a liquid droplet or gas bubble in
another gas and the case of a gas bubble in a liquid.
In those cases the surface tension coefficient :math:`\sigma` introduced in
:math:`p_{st}` in equation (3.19) may be of relevance.
For now, we have only implemented the case where :math:`\sigma = 0`.  This is
generally a good assumption, for compressible particles or liquid droplets in
liquids.

In addition, Doinikov states for some limiting cases of the acoustic radiation
force that this theory is not different from already available theories, e.g.
in section 6.2.1. In those cases, we also did not implement this but raise an
error and point to another model of our framework that covers this special
case.

`Link to paper
<https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/acoustic-radiation-pressure-on-a-compressible-sphere-in-a-viscous-fluid/B945CE378C9D13846F2AD8D072BF0DB0>`_

.. inheritance-diagram::
    osaft.solutions.doinikov1994compressible.arf
   :top-classes: src.solutions.base_arf.BaseARF
   :parts: 1

.. currentmodule:: osaft.solutions.doinikov1994compressible

.. autosummary::
   :toctree: generated/
   :template: template_gallery.rst
   :nosignatures:

   ~base.BaseDoinikov1994Compressible
   ~scattering.CoefficientMatrix
   ~scattering.ScatteringField
   ~arf.ARF
