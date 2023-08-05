.. _Contributing:

Contributing
============

If you'd like to develop or make contributions for OSAFT, fork the
repository from `Gitlab Gorkov Repository`_. If you would like to be even more
involved contact either `ExtremOPS <https://gitlab.com/ExtremOPS>`_ or
`jonas.fankhauser <https://gitlab.com/jonas.fankhauser>`_ directly to be
included into project as a developer.

In any case, pull OSAFT to your computer and install locally with ``pip``::

    pip install -e "/path/to/osaft[dev,docs]"

The option ``[dev,docs]`` ensures that all python packages are installed that
are needed for contribution.

You might want to have it all installed in a virtual python environment. If so,
have a look `here <https://docs.python.org/3/tutorial/venv.html>`_ and follow
the instructions.

In any case, **Pull requests** and **Issues** are absolutely welcome!

Code *Philosophy*
-----------------

Our goal is to have code that is

#. accessible
#. extensive
#. easy to use for users AND developers
#. fully tested and validated

Therefore, we implemented several classes that are used throughout the
different solutions in our :ref:`Core` module. Most solutions differ in the
combination of the used physical model for the :ref:`Fluids`, the physical
model for the :ref:`Solids`, and the :ref:`Backgroundfields`. These core
classes are the foundation for every solution.

We ensure a homogeneous user interface by defining three base classes with
templated methods for the solution of the acoustic scattering problem
(:ref:`BaseScattering`), the solution of the acoustic streaming problem
(:ref:`BaseStreaming`), and also for the solution of the acoustic radiation
force (:ref:`BaseARF`). The solutions to the specific problem **need** to
inherit from the base classes. In addition, if a model implements at least two
of these solutions, we encourage that :ref:`BaseARF` inherits from
:ref:`BaseStreaming` which inherits from :ref:`BaseScattering`.

This reflects also most solutions where the acoustic radiation force is
dependent on the solution to the acoustic streaming problem which is in turn
dependent on the solution for the acoustic scattering problem. For
implementations where just 2 out of the three are implemented, one can also
neglect the missing code inheritance (see :ref:`Yosioka1955`).

Lastly, we utilize the `Observer Design Pattern`_ for the parameters of the
model to reduce redundant computations because the parameter value gets only
recomputed when one of its dependencies changed. The classes
:ref:`ref-osaft.core.variable-PassiveVariable`
and :ref:`ref-osaft.core.variable-ActiveVariable` implement the observer pattern.
A :ref:`ref-osaft.core.variable-PassiveVariable` is the parameter that can be
set. An :ref:`ref-osaft.core.variable-ActiveVariable` is dependent on at least
one passive one. The developer only needs to set the respective links in the
code.

These links, as well as every new introduced methods are tested with our
testsuite. We aim for a coverage of 99% or more to ensure trustworthy code. WE
do not only test for right implementations of methods but also if the theory
produce same results for special limiting cases. Especially the passing of the
physical tests gives the necessary confidence that this code is right.

Coding Style
------------

To adhere to the code style of OSAFT we use the `pre-commit
<https://pre-commit.com>`_ package. This package is automatically installed
when you use the ``[dev,docs]`` option. This package installs a list of
so-called git hooks that check the staged changes before committing. The list of
hooks is available in the `.pre-commit-config.yml
<https://gitlab.com/acoustofluidics/osaft/-/blob/developer/.pre-commit-config.yaml>`_
file. In any case, the pipeline on Gitlab will check before every pull request
if the defined hooks pass.

You setup pre-commit to run automatically on code commits with

.. code-block:: sh

   pre-commit install

This means that every time you commit something the hooks are run first on the
staged files. If one of those fail, you have to fix the errors first before you
are able to commit.

With

.. code-block:: sh

   pre-commit run --all-files

all files will be checked against the hooks.


If you want to bypass the hooks you can use the ``--no-verify`` option with
``git commit``

.. code-block:: sh

   git commit -m "A good descriptive message" --no-verify

Keep in mind that this is just a local bypass. The coding will be tested
anyways on all pull/merge requests.

Testing
-------

We want to have with each new line of code an appropriate test that ensures the
validity of those lines. In some cases, this means to implement a
formula/algorithm/method a second time in the test-suite. This seems tedious
but in the long run it will save hours and nerves when debugging.

Our idea is that each file that introduces a new functionality to the code,
e.g. methods and properties, is tested in a separate file with the same name
plus prefix ``test_`` as the source but located in the ``tests/`` folder. E.g.
the `osaft/core/variable.py
<https://gitlab.com/acoustofluidics/osaft/-/blob/developer/osaft/core/variable.py>`_
file has a testing counterpart under `tests/core/test_variable.py
<https://gitlab.com/acoustofluidics/osaft/-/blob/developer/tests/core/test_variable.py>`_.

There are different ways to run the tests. Many IDEs include it in their GUI to
make it as user-friendly as possible. In any case, you can run from the command
line (the program `coverage <https://coverage.readthedocs.io/en/6.2/>`_ is also
automatically installed with the ``[dev,docs]`` option)

.. code-block:: sh

   coverage run -m unittest discover -v tests/

This will run all tests in the ``tests/`` folder. In order to asses the
coverage of the code you can run either

.. code-block:: sh

   coverage report -m

or

.. code-block:: sh

   coverage html

The first option will print the coverage report to the command line and the
second option will create a folder ``htmlcov/`` which includes a ``index.html``
file. You can open this with any web-browser of you choice and the navigate
through the code to see the untested parts. You can also run both sequentially
with

.. code-block:: sh

   coverage html && coverage report -m

As with the pre-commits, the code will be tested anyways for every merge/pull
request.

Changelog
---------

We want to document the changes/additions/deletions that are applied with every
new merge/pull request. For that we maintain the `CHANGELOG.md
<https://gitlab.com/acoustofluidics/osaft/-/blob/developer/CHANGELOG.md>`_
file. But it is also not just about the documentation. We also want to give
credit to everybody that contributes to OSAFT. In order to do so, please
also adapt this file accordingly when you create a merge/pull request.

Documentation builds
--------------------

As with the testing, we aim for a well documented code. Most of the
documentation will be build anyways because of the ``docstrings`` that are
within the code.

This means that no action other than writing docstrings is necessary if you add
something to already existing code. If, however, you add e.g. a new solution
with the name ``NewSolution2000`` which is highly welcomed and appreciated, you
need to create a ``newsolution2000.rst`` file under ``docs/solutions/``. You
can copy the content from another solution, e.g.
`docs/solutions/yosioka1995.rst
<https://gitlab.com/acoustofluidics/osaft/-/blob/developer/docs/solutions/yosioka1955.rst>`_
, and adapt it accordingly.

To build and view the documentation you need to navigate into

.. code-block:: sh

   cd docs

and build the code

.. code-block:: sh

   make clean html

This command removes all previous builds (``clean``)
and builds a new one in html format (``html``). You can view the build
documentation with your browser by opening ``docs/_build/html/index.html``.


.. _Gitlab Gorkov Repository: https://gitlab.com/acoustofluidics/osaft
.. _Observer Design Pattern: https://en.wikipedia.org/wiki/Observer_pattern
