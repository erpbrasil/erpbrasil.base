
Changelog
=========

0.0.0 (2019-06-07)
~~~~~~~~~~~~~~~~~~

* First release on PyPI.


1.2.0 (2020-07-04)
~~~~~~~~~~~~~~~~~~

* Estabilização da biblioteca


2.0.0 (2020-11-10)
~~~~~~~~~~~~~~~~~~

* Fim do suporte ao python2
* Estabilização dos testes


2.0.1 (2021-04-06)
~~~~~~~~~~~~~~~~~~

* Chave documento fiscal

2.5.0 (não publicada)
~~~~~~~~~~~~~~~~~~~~~

* Empacotamento alinhado às outras libs erpbrasil: extras ``test`` e ``doc``,
  Python 3.7 a 3.14 declarado e testado no CI (3.7 em container), ``__version__``
  lido dos metadados (a versão é a tag do git, via hatch-vcs), publicação com
  ``check-wheel-contents`` e ``twine check``. Saem o ``ci/`` do cookiecutter, o
  ``.bumpversion.cfg`` (apontava para um ``setup.py`` que não existe) e o ``mypy``
  dos extras de teste.
