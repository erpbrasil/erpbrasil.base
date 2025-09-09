========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |ci| |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/erpbrasilbase/badge/?style=flat
    :target: https://readthedocs.org/projects/erpbrasilbase
    :alt: Documentation Status

.. |codecov| image:: https://codecov.io/gh/erpbrasil/erpbrasil.base/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/erpbrasil/erpbrasil.base

.. |version| image:: https://img.shields.io/pypi/v/erpbrasil.base.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/erpbrasil.base

.. |commits-since| image:: https://img.shields.io/github/commits-since/erpbrasil/erpbrasil.base/vvv2.4.1...svg
    :alt: Commits since latest release
    :target: https://github.com/erpbrasil/erpbrasil.base/compare/v1.0.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/erpbrasil.base.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/erpbrasil.base

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/erpbrasil.base.svg
    :alt: Supported versions
    :target: https://pypi.org/project/erpbrasil.base

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/erpbrasil.base.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/erpbrasil.base

.. |ci| image:: https://github.com/erpbrasil/erpbrasil.base/actions/workflows/github-actions.yml/badge.svg
   :target: https://github.com/erpbrasil/erpbrasil.base/actions/workflows/github-actions.yml
   :alt: Build (GitHub Actions)

.. end-badges

erpbrasil.base
##############

Biblioteca python para auxiliar em operações corriqueiras dos ERPs Python Brasileiros:

* Formatação/Validação de CPF/CNPJ, IE, PIS;
* Formatação de CEP;
* Rateio de Frete / Seguro e etc;
* Remoção de pontuação de documentos;
* Chaves de documentos fiscais eletronicos:
    * Geração
    * Validação
    * Conversão em objeto legível

Esta biblioteca faz parte do projeto: https://erpbrasil.github.io/

Documentação
============

https://erpbrasil.github.io/

Créditos
========

Esta é uma biblioteca criada atravês do esforço de das empresas:

* Akretion https://akretion.com/pt-BR/
* KMEE https://www.kmee.com.br

Parte do código foi extraido da localização brasileira do Odoo: https://github.com/oca/l10n-brazil/ favor consultar a lista de contribuidores:

https://github.com/erpbrasil/erpbrasil.base/graphs/contributors

Licença
~~~~~~~

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

Upload to Pypi
==============

Use somente o comando:

 ``twine upload dist/*``

or

 ``twine upload dist/erpbrasil.base-X.X.0.tar.gz --repository-url https://upload.pypi.org/legacy/``
