.. _Installation:

Installation
=======================

OSAFT is available on `PyPI`_. Install `Python`_ **(3.9 or newer)** and run
the following command in your command-line interface

.. code-block:: sh

   pip install osaft

OSAFT is updated to the latest available version via

.. code-block:: sh

   pip install osaft --upgrade

Run the following command in order to remove the package from your system

.. code-block:: sh

   pip uninstall osaft


From now on you can import the OSAFT package in any Python script you like
via

.. code-block:: python3

   ...
   import osaft

   yosioka = osaft.yosioka1955.ARF(
      f=1e6,
      R_0=1e-6,
      rho_s=1.225, c_s=343,
      rho_f=997, c_f=1_4987,
      p_0=1e5,
      wave_type=osaft.WaveType.STANDING,
      position=0,
 )
   ...


.. _PyPi: https://pypi.python.org/pypi/osaft
.. _`Python`: https://www.python.org/
