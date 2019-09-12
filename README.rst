========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/erpbrasilbase/badge/?style=flat
    :target: https://readthedocs.org/projects/erpbrasilbase
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/erpbrasil/erpbrasil.base.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/erpbrasil/erpbrasil.base

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/erpbrasil/erpbrasil.base?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/erpbrasil/erpbrasil.base

.. |codecov| image:: https://codecov.io/gh/erpbrasil/erpbrasil.base/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/erpbrasil/erpbrasil.base

.. |version| image:: https://img.shields.io/pypi/v/erpbrasil.base.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/erpbrasil.base

.. |commits-since| image:: https://img.shields.io/github/commits-since/erpbrasil/erpbrasil.base/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/erpbrasil/erpbrasil.base/compare/v0.0.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/erpbrasil.base.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/erpbrasil.base

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/erpbrasil.base.svg
    :alt: Supported versions
    :target: https://pypi.org/project/erpbrasil.base

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/erpbrasil.base.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/erpbrasil.base


.. end-badges

xBase

* Free software: MIT license

Installation
============

::

    pip install erpbrasil.base

Documentation
=============


https://erpbrasilbase.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
