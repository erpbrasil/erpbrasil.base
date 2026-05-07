============================
Chave dos documentos Fiscais
============================

NF-e - Nota Fiscal Eletrônica
=============================

Chave de Acesso
---------------

A composição da chave de acesso da NF-e sofreu alterações ao longo da evolução do sistema, pela versão 2.00 da NF-e e pela NT 2018.001.

Versão 4.00 da NF-e
-------------------

A Chave de Acesso de identificação da Nota Fiscal eletrônica é um conjunto de 44 caracteres numéricos, formado pela concatenação de campos que se encontram no leiaute da NF-e, seguindo a estrutura que pode ser vista na Tabela

+--------+----------------------------------------------+------------+----------+------------------+ 
|Posição | Informação                                   | Caracteres | Campo    | Id               |
+========+==============================================+============+==========+==================+
| 1      | Código da UF do emitente do Documento Fiscal | 2          | cUF      | B02              |
+--------+----------------------------------------------+------------+----------+------------------+
| 2      | Ano e Mês de emissão da NF-e                 | 4          | AAMM     | Extraídos de B09 |
+--------+----------------------------------------------+------------+----------+------------------+
| 3      | CNPJ/CPF do emitente                         | 14         | CNPJ/CPF | C02/C02a         |
+--------+----------------------------------------------+------------+----------+------------------+
| 4      | Modelo do Documento Fiscal                   | 2          | mod      | B06              |
+--------+----------------------------------------------+------------+----------+------------------+
| 5      | Série do Documento Fiscal                    | 3          | serie    | B07              |
+--------+----------------------------------------------+------------+----------+------------------+
| 6      | Número do Documento Fiscal                   | 9          | nNF      | B08              |
+--------+----------------------------------------------+------------+----------+------------------+
| 7      | forma de emissão da NF-e                     | 1          | tpEmis   | B22              |
+--------+----------------------------------------------+------------+----------+------------------+
| 8      | Código Numérico que compõe a Chave de Acesso | 8          | cNF      | B03              |
+--------+----------------------------------------------+------------+----------+------------------+
| 9      | Dígito Verificador da Chave de Acesso        | 1          | cDV      | B23              |
+--------+----------------------------------------------+------------+----------+------------------+

O Dígito Verificador (DV) garante a integridade da chave de acesso, protegendo-a principalmente contra digitações erradas.
Originalmente, na Chave de Acesso da NF-e deveria ser informado o CNPJ da empresa emitente da NF-e, ou o CNPJ da SEFAZ no caso da Nota Fiscal Avulsa. Esta realidade foi alterada a partir da versão 4.00 do leiaute da NF-e (NT 2018.001), permitindo, a critério da UF, a identificação na Chave de Acesso também de emitente pessoa física (CPF).
Também foi alterado o processo de assinatura da NF-e, que anteriormente somente podia ser feito utilizando um Certificado Digital tipo “e-CNPJ”. No caso do Emitente Pessoa Física:

* O CPF deverá constar na Chave de Acesso, precedido por zeros, completando 14 posições;
* Conforme pode ser visto na Tabela 2-4, está reservada uma faixa do campo Série da NF-e, como forma de identificação do Emitente pessoa física (CPF);
* A NF-e deverá ser assinada com o Certificado Digital do Emitente, do tipo “e-CPF”.

Com exceção do Código Numérico, todas as demais informações que compõem a Chave de Acesso podem ser deduzidas por qualquer pessoa, o que representa um risco importante para a segurança das consultas aos dados das NF-e. Para minimizar este risco, o Código Numérico deve ser uma sequência totalmente aleatória.

Cálculo do Dígito Verificador da Chave de Acesso da NF-e
--------------------------------------------------------

O dígito verificador (DV) da chave de acesso da NF-e é baseado em um cálculo do módulo 11. O módulo 11 de um número é calculado multiplicando-se cada algarismo pela sequência de números 2,3,4,5,6,7,8,9,2,3, ..., posicionados da direita para a esquerda. A somatória dos resultados das ponderações dos algarismos é dividida por 11 e o DV (dígito verificador) será a diferença entre o divisor (11) e o resto da divisão:

DV = 11 - (resto da divisão)

Quando o resto da divisão for 0 (zero) ou 1 (um), o DV deverá ser igual a 0 (zero).

Exemplo:

Consideremos uma chave de acesso com a seguinte sequência de caracteres:

+--------------------+----+---+---+----+---+----+----+----+---+---+----+----+---+---+---+---+---+----+---+----+----+----+---+---+---+---+---+---+---+---+---+----+----+---+---+----+----+----+----+---+---+----+---+
| A. CHAVE DE ACESSO | 5  | 2 | 0 | 6  | 0 | 4  | 3  | 3  | 0 | 0 | 9  | 9  | 1 | 1 | 0 | 0 | 2 | 5  | 0 | 6  | 5  | 5  | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 7  | 8  | 0 | 0 | 2  | 6  | 7  | 3  | 0 | 1 | 6  | 1 |
+====================+====+===+===+====+===+====+====+====+===+===+====+====+===+===+===+===+===+====+===+====+====+====+===+===+===+===+===+===+===+===+===+====+====+===+===+====+====+====+====+===+===+====+===+
| B. PESOS           | 4  | 3 | 2 | 9  | 8 | 7  | 6  | 5  | 4 | 3 | 2  | 9  | 8 | 7 | 6 | 5 | 4 | 3  | 2 | 9  | 8  | 7  | 6 | 5 | 4 | 3 | 2 | 9 | 8 | 7 | 6 | 5  | 4  | 3 | 2 | 9  | 8  | 7  | 6  | 5 | 4 | 3  | 2 |
+--------------------+----+---+---+----+---+----+----+----+---+---+----+----+---+---+---+---+---+----+---+----+----+----+---+---+---+---+---+---+---+---+---+----+----+---+---+----+----+----+----+---+---+----+---+
| C. PONDERAÇÃO(A*B) | 20 | 6 | 0 | 54 | 0 | 28 | 18 | 15 | 0 | 0 | 18 | 81 | 8 | 7 | 0 | 0 | 8 | 15 | 0 | 54 | 40 | 35 | 0 | 5 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 35 | 32 | 0 | 0 | 18 | 48 | 49 | 18 | 0 | 4 | 18 | 2 |
+--------------------+----+---+---+----+---+----+----+----+---+---+----+----+---+---+---+---+---+----+---+----+----+----+---+---+---+---+---+---+---+---+---+----+----+---+---+----+----+----+----+---+---+----+---+

Somatória das ponderações = 644

Dividindo a somatória das ponderações por 11 teremos 644 / 11 = 58 restando 6. DV = 11 - (resto da divisão) = 11 - 6 = 5

Neste caso o DV da chave de acesso da NF-e é igual a "5", valor este que deverá compor a chave de acesso, formando uma sequência de 44 caracteres.

Versões anteriores ao leiaute 4.00 da NF-e
------------------------------------------

Até a versão 1.10 do leiaute da NF-e, a Chave de Acesso da Nota Fiscal Eletrônica foi composta pela caracteres numéricos exposta na Tabela abaixo:

+-------------------+-----------------+------------------+-------------+--------------+---------------------+----------------------+----------+
| Código da UF(cUF) | AAMM da Emissão | CNPJ do Emitente | Modelo(mod) | Série(serie) | Número da NF-e(nNF) | Código Numérico(cNF) | DV(cDV)  |
+===================+=================+==================+=============+==============+=====================+======================+==========+
| 2 digitos         | 4 digitos       | 14 digitos       | 2 digitos   | 3 digitos    | 9 digitos           | 9 digitos            | 1 digito |
+-------------------+-----------------+------------------+-------------+--------------+---------------------+----------------------+----------+

A partir da versão 2.00 do leiaute da NF-e, o campo tpEmis (forma de emissão da NF-e) passou a compor a chave de acesso. Para que o tamanho de 44 posições da chave não fosse alterado, o tamanho do campo cNF (código numérico da NF-e) foi reduzido para oito posições, conforme pode ser visto na Tabela abaixo:

+-------------------+-----------------+------------------------+-------------+--------------+---------------------+----------------------------------+-----------------------+----------+
| Código da UF(cUF) | AAMM da Emissão | CNPJ do Emitente(CNPJ) | Modelo(mod) | Série(serie) | Número da NF-e(nNF) | Forma de emissão da NF-e(tpEmis) | Código Numérico.      | DV(cDV)  |
+===================+=================+========================+=============+==============+=====================+==================================+=======================+==========+
| 2 digitos         | 4 digitos       | 14 digitos             | 2 digitos   | 3 digitos    | 9 digitos           | 1 digito                         | 8 digitos             | 1 digito |
+-------------------+-----------------+------------------------+-------------+--------------+---------------------+----------------------------------+-----------------------+----------+

A legislação determina que a identificação única de uma nota fiscal para efeitos tributários é feita pelos seguintes conjuntos de informações, que são um subconjunto das informações existentes na chave de acesso:

* **NF-e:** UF, CNPJ ou CPF do Emitente, Série e Número da NF-e, modelo do documento fiscal eletrônico e ambiente de autorização.
* **NFC-e:** UF, CNPJ do Emitente, Série e Número da NF-e, modelo do documento fiscal eletrônico e tipo de emissão.

Estes subconjuntos recebem a denominação de “chave natural” (NT 2018.001), sendo que o ambiente de autorização e o tipo de emissão aparecem no campo tpEmis (id: B22).
O Sistema de Autorização de Uso da SEFAZ valida a existência de uma NF-e previamente autorizada e rejeita novos pedidos de autorização para NF-e caso seja identificada duplicidade de Chave Natural.

Série Reservadas da NF-e
------------------------

O campo Série da NF-e (id:B07) também é utilizado para auxiliar, juntamente com o campo procEmi (id: B26), no controle das emissões e identificação do processo de emissão, conforme descrito na Tabela abaixo:

+------------+------------------------+----------------------------------------------------------------+-------------+------------------+--------------------------------------------------------------------+
| Emit       | Processo Emissão       | Assinatura                                                     | Série       | Chave de Acesso  | Numeração                                                          |
+============+========================+================================================================+=============+==================+====================================================================+
| CNPJ       | Aplicativo da Empresa  | e-CNPJ do Emitente (procEmi <> 1,2)                            | 000 até 889 | CNPJ do Emitente | Sequencial por CNPJ, controlado pelo emitente                      |
+------------+------------------------+----------------------------------------------------------------+-------------+------------------+--------------------------------------------------------------------+
| CNPJ       | Programa Emissor Fisco | e-CNPJ do Emitente (procEmi <> 1,2)                            | 000 até 889 | CNPJ do Emitente | Sequencial por CNPJ, controlado pelo emitente                      |
+------------+------------------------+----------------------------------------------------------------+-------------+------------------+--------------------------------------------------------------------+
| CNPJ / CPF | Site SEFAZ (NFA-e)     | e-CNPJ da SEFAZ (procEmi=1)                                    | 890 até 899 | CNPJ da SEFAZ    | Sequencial pela SEFAZ, independentemente do emitente (CPF ou CNPJ) |
+------------+------------------------+----------------------------------------------------------------+-------------+------------------+--------------------------------------------------------------------+
| Faixas reservadas a partir da NT 2018.001                                                                                                                                                                  |
+------------+------------------------+----------------------------------------------------------------+-------------+------------------+--------------------------------------------------------------------+
| CNPJ       | Site SEFAZ             | e-CNPJ da SEFAZ (procEmi=1), ou e-CNPJ do Emitente (procEmi=2) | 900 até 909 | CNPJ do Emitente | Sequencial por CNPJ, controlado pela SEFAZ                         |
+------------+------------------------+----------------------------------------------------------------+-------------+------------------+--------------------------------------------------------------------+
| CPF        | Site SEFAZ             | e-CNPJ da SEFAZ (procEmi=1), ou e-CPF do Emitente (procEmi=2)  | 910 até 919 | CPF do Emitente  | Sequencial pelo CPF, controlado pela SEFAZ                         |
+------------+------------------------+----------------------------------------------------------------+-------------+------------------+--------------------------------------------------------------------+
| CPF        | Aplicativo da Empresa  | e-CPF do Emitente (procEmi<>1,2)                               | 920 até 969 | CPF do Emitente  | Sequencial por CPF, controlado pelo emitente                       |
+------------+------------------------+----------------------------------------------------------------+-------------+------------------+--------------------------------------------------------------------+



Importante comentar que normalmente o CNPJ define um único estabelecimento (uma única filial da empresa na UF), com um único endereço e uma única Inscrição Estadual.

No caso do Produtor Primário isto muda, e podem existir casos onde o mesmo CNPJ participa de vários Estabelecimentos (várias Inscrições Estaduais). Nestes casos, o CNPJ na Chave de Acesso pode não identificar uma única Inscrição Estadual na UF.

O mesmo ocorre para o Produtor Primário identificado pelo seu CPF, sendo mais comum ainda a participação do mesmo CPF em diferentes estabelecimentos (várias Inscrições Estaduais de Produtor Primário) na mesma UF.

Numeração da NF-e por Estabelecimento Rural (Inscrição Estadual)
----------------------------------------------------------------

No caso de Produtor Primário, Pessoa Física, na Chave de Acesso consta o CPF do Emitente, mas não consta a Inscrição Estadual.

Esta realidade traz uma dificuldade para poder gerenciar a numeração das NF-e por Inscrição Estadual, caso o CPF participe em vários estabelecimentos rurais.

Exemplificando, para o mesmo CPF, a NF-e número 1 pode ser autorizada por uma determinada Inscrição Estadual e a NF-e número 2 pode ter sido autorizada para outra Inscrição Estadual de Produtor Primário.

Nestes casos, o contribuinte deverá utilizar Séries específicas para cada estabelecimento, na faixa 920 a 969.

CT-e - Conhecimento de Transporte
=================================

Chave de Acesso do CTe
----------------------

A Chave de Acesso do CTe é composta pelos seguintes campos que se encontram dispersos no leiaute do CTe:

+-------------------+-----------------+------------------------+-------------+--------------+---------------------+----------------------------------+-----------------------+----------+
| Código da UF(cUF) | AAMM da Emissão | CNPJ do Emitente(CNPJ) | Modelo(mod) | Série(serie) | Número do BP-e(nNF) | Forma de emissão do BP-e(tpEmis) | Código Numérico(cBPe) | DV(cDV)  |
+===================+=================+========================+=============+==============+=====================+==================================+=======================+==========+
| 2 digitos         | 4 digitos       | 14 digitos             | 2 digitos   | 3 digitos    | 9 digitos           | 1 digito                         | 8 digitos             | 1 digito |
+-------------------+-----------------+------------------------+-------------+--------------+---------------------+----------------------------------+-----------------------+----------+

* **cUF** - Código da UF do emitente do Documento Fiscal
* **AAMM** - Ano e Mês de emissão do CTe
* **CNPJ** - CNPJ do emitente
* **mod** - Modelo do Documento Fiscal
* **serie** - Série do Documento Fiscal
* **nCT** - Número do Documento Fiscal
* **tpEmis** - forma de emissão do CTe
* **cCT** - Código Numérico que compõe a Chave de Acesso
* **cDV** - Dígito Verificador da Chave de Acesso

O Dígito Verificador (DV) irá garantir a integridade da chave de acesso, protegendo-a principalmente contra digitações erradas.

Chave Natural do CTe
--------------------

A Chave Natural do CTe é composta pelos campos de UF, CNPJ/CPF do Emitente, Série e Número do CTe, além do modelo do documento fiscal eletrônico e sua forma de emissão. O Sistema de Autorização de Uso das SEFAZ valida a existência de um CTe previamente autorizado e rejeita novos pedidos de autorização para CTe com duplicidade da Chave Natural.


BP-e - Bilhete de Passagem Eletrônico
=====================================

Chave de acesso do BP-e
-----------------------

A Chave de Acesso do BP-e é composta pelos seguintes campos que se encontram dispersos no leiaute do BP-e:

+-------------------+-----------------+------------------------+-------------+--------------+---------------------+----------------------------------+-----------------------+----------+
| Código da UF(cUF) | AAMM da Emissão | CNPJ do Emitente(CNPJ) | Modelo(mod) | Série(serie) | Número do CT-e(nCT) | Forma de emissão do CT-e(tpEmis) | Código Numérico.      | DV(cDV)  |
+===================+=================+========================+=============+==============+=====================+==================================+=======================+==========+
| 2 digitos         | 4 digitos       | 14 digitos             | 2 digitos   | 3 digitos    | 9 digitos           | 1 digito                         | 8 digitos             | 1 digito |
+-------------------+-----------------+------------------------+-------------+--------------+---------------------+----------------------------------+-----------------------+----------+

* **cUF** - Código da UF do emitente do Documento Fiscal
* **AAMM** - Ano e Mês de emissão do BP-e
* **CNPJ** - CNPJ do emitente
* **mod** - Modelo do Documento Fiscal
* **serie** - Série do Documento Fiscal
* **nNF** - Número do Documento Fiscal
* **tpEmis** - forma de emissão do BP-e
* **cBPe** - Código Numérico que compõe a Chave de Acesso
* **cDV** - Dígito Verificador da Chave de Acesso

O Dígito Verificador (DV) irá garantir a integridade da chave de acesso, protegendo-a principalmente contra digitações erradas.

Chave Natural do BP-e
---------------------

A Chave Natural do BP-e é composta pelos campos de UF, CNPJ do Emitente, Série e Número do BP-e, além do modelo do documento fiscal eletrônico. O Sistema de Autorização de Uso da SEFAZ valida a existência de um BP-e previamente autorizado e rejeita novos pedidos de autorização para BP-e com duplicidade da Chave Natural.

NF3e - Nota Fiscal de Energia Elétrica Eletrônica
=================================================

Chave de Acesso da NF3e
-----------------------

A Chave de Acesso da NF3e é composta pelos seguintes campos que se encontram dispersos no leiaute da NF3e:

+-------------------+-----------------+------------------------+-------------+--------------+---------------------+----------------------------------+-----------------------------+------------------------+----------+
| Código da UF(cUF) | AAMM da Emissão | CNPJ do Emitente(CNPJ) | Modelo(mod) | Série(serie) | Número do NF3e(nNF) | Forma de emissão da NF3e(tpEmis) | Site Autoriz.(nSiteAutoriz) | Código Numérico(cNF3e) | DV(cDV)  |
+===================+=================+========================+=============+==============+=====================+==================================+=============================+========================+==========+
| 2 digitos         | 4 digitos       | 14 digitos             | 2 digitos   | 3 digitos    | 9 digitos           | 1 digito                         | 1 digito                    | 7 digitos              | 1 digito |
+-------------------+-----------------+------------------------+-------------+--------------+---------------------+----------------------------------+-----------------------------+------------------------+----------+

* **cUF** - Código da UF do emitente do Documento Fiscal
* **AAMM** - Ano e Mês de emissão da NF3e
* **CNPJ** - CNPJ do emitente
* **mod** - Modelo do Documento Fiscal
* **serie** - Série do Documento Fiscal
* **nNF** - Número do Documento Fiscal
* **tpEmis** - forma de emissão da NF3e
* **nSiteAutoriz** – Site do Autorizador que recepcionou a NF3e
* **cNF3e** - Código Numérico que compõe a Chave de Acesso
* **cDV** - Dígito Verificador da Chave de Acesso

O Dígito Verificador (DV) irá garantir a integridade da chave de acesso, protegendo-a principalmente contra digitações erradas.

Chave Natural da NF3e
---------------------

A Chave Natural da NF3e é composta pelos campos de UF, CNPJ do Emitente, Série e Número da NF3e, além do modelo do documento fiscal eletrônico, forma de emissão e do Site em que ela foi autorizada. O Sistema de Autorização de Uso da SEFAZ valida a existência de uma NF3e previamente autorizada e rejeita novos pedidos de autorização para NF3e com duplicidade da Chave Natural quando autorizados no mesmo ambiente de autorização. A informação da Forma de Emissão e do Site em que foi Autorizada a NF3e podem indicar ambientes alternativos de autorização da SEFAZ.

NFAg - Nota Fiscal de Água e Saneamento Eletrônica
==================================================

Chave de Acesso da NFAg
-----------------------

A Chave de Acesso da NFAg é composta pelos seguintes campos que se encontram dispersos no leiaute da NFAg:

+-------------------+-----------------+------------------------+-------------+--------------+---------------------+----------------------------------+-----------------------------+------------------------+----------+
| Código da UF(cUF) | AAMM da Emissão | CNPJ do Emitente(CNPJ) | Modelo(mod) | Série(serie) | Número da NFAg(nNF) | Forma de emissão da NFAg(tpEmis) | Site Autoriz.(nSiteAutoriz) | Código Numérico        | DV(cDV)  |
+===================+=================+========================+=============+==============+=====================+==================================+=============================+========================+==========+
| 2 digitos         | 4 digitos       | 14 digitos             | 2 digitos   | 3 digitos    | 9 digitos           | 1 digito                         | 1 digito                    | 7 digitos              | 1 digito |
+-------------------+-----------------+------------------------+-------------+--------------+---------------------+----------------------------------+-----------------------------+------------------------+----------+

* **cUF** - Código da UF do emitente do Documento Fiscal
* **AAMM** - Ano e Mês de emissão da NFAg
* **CNPJ** - CNPJ do emitente
* **mod** - Modelo do Documento Fiscal (75)
* **serie** - Série do Documento Fiscal
* **nNF** - Número do Documento Fiscal
* **tpEmis** - forma de emissão da NFAg (1 – Normal, 2 – Contingência Offline)
* **nSiteAutoriz** – Site do Autorizador que recepcionou a NFAG
* **cNF** - Código Numérico aleatório que compõe a Chave de Acesso
* **cDV** - Dígito Verificador da Chave de Acesso

O Dígito Verificador (DV) irá garantir a integridade da chave de acesso, protegendo-a principalmente contra digitações erradas.

Chave Natural da NFAg
---------------------

A Chave Natural da NFAg é composta pelos campos de UF, CNPJ do Emitente, Série e Número da NFAg, além do modelo do documento fiscal eletrônico, da forma de emissão e do Site em que ela foi autorizada. O Sistema de Autorização de Uso validará a existência de uma NFAg previamente autorizada e rejeitará novos pedidos de autorização para NFAg com duplicidade da Chave Natural, quando autorizados no mesmo ambiente de autorização. A informação da Forma de Emissão e do Site em que foi Autorizada a NFAg podem indicar ambientes alternativos de autorização do Ambiente Nacional.

NFCom - Nota Fiscal Fatura de Serviço de Comunicação Eletrônica
===============================================================

Chave de Acesso da NFCom
------------------------

A Chave de Acesso da NFCom é composta pelos seguintes campos que se encontram dispersos no leiaute da NFCom:

+-------------------+-----------------+------------------------+-------------+--------------+----------------------+-----------------------------------+-----------------------------+------------------------+----------+
| Código da UF(cUF) | AAMM da Emissão | CNPJ do Emitente(CNPJ) | Modelo(mod) | Série(serie) | Número da NFCom(nNF) | Forma de emissão da NFCom(tpEmis) | Site Autoriz.(nSiteAutoriz) | Código Numérico        | DV(cDV)  |
+===================+=================+========================+=============+==============+======================+===================================+=============================+========================+==========+
| 2 digitos         | 4 digitos       | 14 digitos             | 2 digitos   | 3 digitos    | 9 digitos            | 1 digito                          | 1 digito                    | 7 digitos              | 1 digito |
+-------------------+-----------------+------------------------+-------------+--------------+----------------------+-----------------------------------+-----------------------------+------------------------+----------+

* **cUF** - Código da UF do emitente do Documento Fiscal
* **AAMM** - Ano e Mês de emissão da NFCom
* **CNPJ** - CNPJ do emitente
* **mod** - Modelo do Documento Fiscal
* **serie** - Série do Documento Fiscal
* **nNF** - Número do Documento Fiscal
* **tpEmis** - forma de emissão da NFCom
* **nSiteAutoriz** – Site do Autorizador que recepcionou a NFCOM
* **cNFCom** - Código Numérico que compõe a Chave de Acesso
* **cDV** - Dígito Verificador da Chave de Acesso

O Dígito Verificador (DV) irá garantir a integridade da chave de acesso, protegendo-a principalmente contra digitações erradas.

Chave Natural da NFCom
----------------------

A Chave Natural da NFCom é composta pelos campos de UF, CNPJ do Emitente, Série e Número da NFCom, além do modelo do documento fiscal eletrônico, forma de emissão e do Site em que ela foi autorizada. O Sistema de Autorização de Uso da SEFAZ valida a existência de uma NFCom previamente autorizada e rejeita novos pedidos de autorização para NFCom com duplicidade da Chave Natural quando autorizados no mesmo ambiente de autorização. A informação da Forma de Emissão e do Site em que foi Autorizada a NFCom podem indicar ambientes alternativos de autorização da SEFAZ.

NFGas - Nota Fiscal Eletrônica do Gás
=====================================

Chave de Acesso da NFGas
------------------------

A Chave de Acesso da NFGas é composta pelos seguintes campos que se encontram dispersos no leiaute da NFGas:

+-------------------+-----------------+------------------------+-------------+--------------+----------------------+-----------------------------------+-----------------------------+------------------------+----------+
| Código da UF(cUF) | AAMM da Emissão | CNPJ do Emitente(CNPJ) | Modelo(mod) | Série(serie) | Número da NFGas(nNF) | Forma de emissão da NFGas(tpEmis) | Site Autoriz.(nSiteAutoriz) | Código Numérico        | DV(cDV)  |
+===================+=================+========================+=============+==============+======================+===================================+=============================+========================+==========+
| 2 digitos         | 4 digitos       | 14 digitos             | 2 digitos   | 3 digitos    | 9 digitos            | 1 digito                          | 1 digito                    | 7 digitos              | 1 digito |
+-------------------+-----------------+------------------------+-------------+--------------+----------------------+-----------------------------------+-----------------------------+------------------------+----------+


* **cUF** - Código da UF do emitente do Documento Fiscal
* **AAMM** - Ano e Mês de emissão da NFGas
* **CNPJ** - CNPJ do emitente
* **mod** - Modelo do Documento Fiscal (76)
* **serie** - Série do Documento Fiscal
* **nNF** - Número do Documento Fiscal
* **tpEmis** - forma de emissão da NFGas (1 – Normal, 2 – Contingência Offline)
* **nSiteAutoriz** – Site do Autorizador que recepcionou a NFGAS
* **cNF** - Código Numérico aleatório que compõe a Chave de Acesso
* **cDV** - Dígito Verificador da Chave de Acesso

O Dígito Verificador (DV) irá garantir a integridade da chave de acesso, protegendo-a principalmente contra digitações erradas.

Chave Natural da NFGas
----------------------

A Chave Natural da NFGas é composta pelos campos de UF, CNPJ do Emitente, Série e Número da NFGas, além do modelo do documento fiscal eletrônico, da forma de emissão e do Site em que ela foi autorizada. O Sistema de Autorização de Uso validará a existência de uma NFGas previamente autorizada e rejeitará novos pedidos de autorização para NFGas com duplicidade da Chave Natural, quando autorizados no mesmo ambiente de autorização. A informação da Forma de Emissão e do Site em que foi Autorizada a NFGas podem indicar ambientes alternativos de autorização do Ambiente Nacional.

NFS-e - Nota Fiscal de Serviço Eletrônica
=========================================

Chave de Acesso da NFS-e
------------------------

A Chave de Acesso da NFS-e é composta pelos seguintes campos que se encontram dispersos no leiaute da NFS-e:

+-------------------+----------------------+---------------------------+------------------------------+------------------------+----------------+-----------------------------------+
| Cód. Munic.(cMun) | Amb. Gerador(ambGer) | Tipo de Inscrição Federal | Inscrição Federal (CNPJ/CPF) | Número da NFS-e(nNFSe) | AnoMes Emissão | Código Numérico        | DV(cDV)  |
+===================+======================+===========================+==============================+========================+======================+=============================+
| 7 digitos         | 1 digito             | 1 digito                  | 14 digitos                   | 13 digitos             | 4 digitos      | 9 digitos            | 1 digito   |
+-------------------+----------------------+---------------------------+------------------------------+------------------------+----------------+-----------------------------------+


* **cMun** - Código do Município do emitente do Documento Fiscal
* **ambGer** - Ambiente gerador da NFS-e: 1 - Sistema Próprio do Município; 2 - Sefin Nacional NFS-e.
* **Tipo de Inscrição Federal** - Tipo de Inscrição Federal do emitente: 1 - CPF; 2 - CNPJ.
* **Inscrição Federal** - CPF ou CNPJ do emitente
* **nNFSe** - Número da NFS-e
* **AAMM** - Ano e Mês de emissão da NFS-e
* **cNF** - Código Numérico aleatório que compõe a Chave de Acesso
* **cDV** - Dígito Verificador da Chave de Acesso
