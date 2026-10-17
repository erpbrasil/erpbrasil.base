
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

2.5.0 (2026-10-15)
~~~~~~~~~~~~~~~~~~

* Chave de acesso com CNPJ alfanumérico (NT Conjunta 2025.001): as 12 primeiras
  posições do CNPJ do emitente na chave aceitam letras maiúsculas e o DV usa o
  valor ASCII - 48 de cada caractere (``misc.modulo11``). A validação do CNPJ
  alfanumérico passa a aceitar as letras I, O, U, Q e F, cuja exclusão era só
  uma solicitação do ENCAT, não confirmada pela Receita Federal (#67).
* Código numérico da chave (cNF, cCT, cMDF) sorteado com ``secrets``, como pede
  o MOC, descartando os valores da rejeição 897 e o número do documento. O
  cálculo antigo, derivado dos campos da chave, fica como
  ``calculo_codigo_aleatorio`` (legado). Quem precisa remontar a mesma chave deve
  guardar o código gerado e informá-lo em ``codigo_aleatorio`` (#69).
* Geração e validação das chaves de DF-e em ``fiscal/dfe.py`` (``ChaveDFe``,
  ``ChaveCFeSAT``, ``ChaveNFSe`` e ``detectar_chave_dfe``): nomes oficiais dos
  campos do XML ao lado dos legados, ``nSiteAutoriz``, os modelos NFCom (62),
  BPe (63), NF3e (66), NFAg (75) e NFGas (76) e a chave de 50 posições da NFS-e
  Nacional. ``fiscal/edoc.py`` continua importável como camada de
  compatibilidade (``ChaveEdoc`` e ``detectar_chave_edoc``). Atenção: passe os
  campos do ``ChaveEdoc`` por nome, porque a ordem dos argumentos posicionais
  depois da chave mudou, e importe ``modulo11`` e ``punctuation_rm`` de
  ``erpbrasil.base.misc`` (#74, a partir do #62 de Renato Lima).
* Empacotamento alinhado às outras libs erpbrasil: extras ``test`` e ``doc``,
  Python 3.7 a 3.14 declarado e testado no CI (3.7 em container), ``__version__``
  lido dos metadados (a versão é a tag do git, via hatch-vcs), publicação com
  ``check-wheel-contents`` e ``twine check``. Saem o ``ci/`` do cookiecutter, o
  ``.bumpversion.cfg`` (apontava para um ``setup.py`` que não existe) e o ``mypy``
  dos extras de teste (#70).
* Actions do CI atualizadas: ``checkout`` v7, ``setup-python`` v7 e
  ``codecov-action`` v7 (#71, #72 e #73).


2.5.1 (2026-10-17)
~~~~~~~~~~~~~~~~~~

* Inscrição estadual de MS: aceita a numeração nova iniciada por 50, do novo
  cadastro fiscal da SEFAZ-MS (e-CCE, para comércio, indústria e serviço), além
  da iniciada por 28 (inscrições antigas e cadastro rural). O cálculo do dígito
  verificador é o mesmo (#76).
