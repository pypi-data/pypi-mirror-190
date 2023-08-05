Welcome to OSAFT's documentation!
==============================================

Welcome to the documentation of the Open Source Acoustofluidics Theory
(OSAFT) Library. OSAFT is a Python library for acoustofluidics that
implements classical theories focusing on the computation of the acoustic
radiation force.

Getting started
-------------------

Install the OSAFT package now using ``pip``

.. code-block:: sh

   pip install osaft

Or go to :ref:`Installation` for more information on the installation
process. Learn how to use the package by going to the :ref:`Examples` section.
The more detailed documentation can be found in the :ref:`Module` section.
We are always looking for
support in further developing our package. Go to
:ref:`Contributing` if you would like to help.


Available Models
-------------------

There are currently six different theories available in OSAFT and more are
under development. Depending on the theory it is possible to evaluate the
scattering field, the streaming field, or the acoustic radiation force of a
model.

.. toctree::
   :hidden:

   installation
   examples/index
   module
   contributing

.. list-table::
   :widths: auto
   :header-rows: 1

   * - Name
     - Scattering
     - Streaming
     - ARF
   * - :ref:`King1934`
     - ✓
     - \-
     - ✓
   * - :ref:`Yosioka1955`
     - ✓
     - \-
     - ✓
   * - :ref:`Gorkov1962`
     - \-
     - \-
     - ✓
   * - :ref:`Hasegawa1969`
     - ✓
     - \-
     - ✓
   * - :ref:`Doinikov1994Rigid`
     - ✓
     - \-
     - ✓
   * - :ref:`Doinikov1994Compressible`
     - ✓
     - \-
     - ✓
   * - :ref:`Settnes2012`
     - \-
     - \-
     - ✓
   * - :ref:`Doinikov2021Viscous`
     - ✓
     - ✗
     - ✓
   * - :ref:`Doinikov2021Viscoelastic`
     - ✓
     - ✗
     - ✗

Plotting Functionalities
--------------------------

OSAFT offers plotting functionalities. Our plotting classes are listed in
the :ref:`Plotting` documentation.

.. _CitingOsaft:

Publication / Citing OSAFT
-------------------------------

.. _Frontiers in Physics: https://www.frontiersin.org/journals/physics
.. _this link: https://www.frontiersin.org/article/10.3389/fphy.2022.893686

The module is published in `Frontiers in Physics`_ under open-access and
available with `this link`_. If you use the framework please use the following
``BibTeX`` key for referencing OSAFT.

.. code-block:: sh

   @ARTICLE{Fankhauser2022,
    AUTHOR={Fankhauser, Jonas and Goering, Christoph and Dual, Jürg},
    TITLE={{OSAFT Library: An Open-Source Python Library for Acoustofluidics}},
    JOURNAL={Frontiers in Physics},
    VOLUME={10},
    YEAR={2022},
    URL={https://www.frontiersin.org/article/10.3389/fphy.2022.893686},
    DOI={10.3389/fphy.2022.893686},
    ISSN={2296-424X},
   }
