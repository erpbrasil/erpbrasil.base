================================
CNPJ Alfanumérico (NT 2025.001)
================================

Introdução
==========

A Receita Federal do Brasil publicou a Instrução Normativa 2229 de 15 de outubro de 2024
que modifica a regra de formação do CNPJ no Brasil. Essa ação visa ampliar a capacidade
de geração de números de CNPJ para abertura de empresas devido ao esgotamento da
modelagem atual.

A previsão de geração dos primeiros CNPJ Alfanuméricos está definida para **julho de 2026**.

Esta nota técnica abrange os ambientes de autorização de documentos fiscais eletrônicos
sob a coordenação do ENCAT:

* NF-e
* NFC-e
* CT-e
* CT-e OS
* GTVe
* MDF-e
* BP-e
* BP-e TM
* NF3e
* NFCom

**Cronograma de implantação:**

+----------+-------------------------------+----------------------------+----------------------+
| Versão   | Histórico                     | Implantação Homologação    | Implantação Produção |
+==========+===============================+============================+======================+
| 1.00     | Versão inicial da NT Conjunta | 06/04/2026                 | 06/07/2026           |
+----------+-------------------------------+----------------------------+----------------------+

Nova Lei de Formação do CNPJ
=============================

O novo número de identificação — **CNPJ Alfanumérico** — terá o mesmo tamanho que o
número atual, com **14 posições**, distribuídas da seguinte forma:

+-------------------+--------------------+-------------------+
| Raiz (8 posições) | Ordem (4 posições) | DV (2 posições)   |
+===================+====================+===================+
| Alfanumérica      | Alfanumérica       | Numérica          |
+-------------------+--------------------+-------------------+

* As **oito primeiras posições** (raiz) terão caracteres alfanuméricos (letras e números).
* As **quatro posições seguintes** (ordem do estabelecimento) também terão caracteres
  alfanuméricos.
* As **duas últimas posições** são numéricas e identificam os dígitos verificadores.

Cálculo do Dígito Verificador do CNPJ Alfanumérico
----------------------------------------------------

A fórmula de cálculo do dígito verificador **não muda**: continua sendo pelo **módulo 11**.
Porém, para garantir compatibilidade com CNPJs puramente numéricos existentes, altera-se
o modo de obtenção dos valores usados no cálculo:

* Cada caractere (numérico ou alfabético) é substituído pelo valor decimal correspondente
  ao seu código ASCII menos 48.
* Desta forma, os dígitos numéricos mantêm os mesmos valores (``'0'`` → 0, ``'9'`` → 9).
* As letras assumem os valores: ``A`` = 17, ``B`` = 18, ``C`` = 19 … e assim por diante.

Pesos utilizados no cálculo (posições 1 a 13, da esquerda para a direita)::

    Posição: 1  2  3  4  5  6  7  8  9  10 11 12 13
    Peso DV1: 5  4  3  2  9  8  7  6  5  4  3  2  -
    Peso DV2: 6  5  4  3  2  9  8  7  6  5  4  3  2

Algoritmo (módulo 11):

1. Para cada um dos 12 primeiros caracteres (sem os DVs), calcule ``valor_ascii - 48``.
2. Multiplique pelo peso correspondente e some os resultados → ``soma_dv1``.
3. ``dv1 = 0`` se ``soma_dv1 % 11 < 2``, senão ``dv1 = 11 - (soma_dv1 % 11)``.
4. Repita o processo incluindo ``dv1`` com peso 2 → ``soma_dv2``.
5. ``dv2 = 0`` se ``soma_dv2 % 11 < 2``, senão ``dv2 = 11 - (soma_dv2 % 11)``.

Letras não permitidas
---------------------

Algumas letras **não devem ser aceitas** no CNPJ Alfa por solicitação do ENCAT à
Receita Federal:

* ``I`` (letra i maiúscula)
* ``O`` (letra o maiúscula)
* ``U`` (letra u maiúscula)
* ``Q`` (letra q maiúscula)
* ``F`` (letra f maiúscula)

.. note::
   Esta exclusão faz parte das solicitações feitas pela equipe técnica do ENCAT para a
   Receita Federal do Brasil e precisa ser confirmada em versão posterior da nota técnica.

Campos do Tipo CNPJ nos DFe
============================

A expressão regular que valida um campo do tipo CNPJ nos schemas XSD passa a aceitar
letras maiúsculas nas primeiras 12 posições::

    [A-Z0-9]{12}[0-9]{2}

Os campos que representam um CNPJ existem dispostos diversas vezes em todos os DFe,
eventos e schemas de serviços disponíveis (emitente, destinatário, tomador, comprador,
recebedor, expedidor, etc.).

Regras de Validação
-------------------

A redação das regras de validação existentes **não se altera**: elas continuam indicando
que o CNPJ informado deve ser válido em relação ao DV.

A partir da data de implantação, os ambientes autorizadores considerarão o novo cálculo
de DV tanto para CNPJs numéricos quanto alfanuméricos. As rejeições já existentes
continuarão sendo aplicadas.

.. important::
   As rotinas de validação de CNPJ devem rejeitar CNPJ Alfanuméricos informados
   **anteriores à data de implantação** de cada ambiente (homologação e produção),
   mesmo que seja admitida a informação na validação de schema. A rejeição aplicada
   nesse caso será a de falha no cálculo do dígito verificador.

Chave de Acesso com CNPJ Alfanumérico
======================================

A chave de acesso de qualquer DFe possui estrutura de 44 posições, sendo que as posições
do CNPJ (posições 7 a 20) podem agora conter caracteres alfanuméricos:

+--------+---------+------------------+-------+-------+--------+--------+---------+----+
| cUF    | AAMM    | CNPJ Emitente    | mod   | serie | nNF    | tpEmis | cXXX    | cDV|
+========+=========+==================+=======+=======+========+========+=========+====+
| 2 dig. | 4 dig.  | 14 dig. (alfa)   | 2 dig | 3 dig | 9 dig. | 1 dig. | 8 dig.  | 1  |
+--------+---------+------------------+-------+-------+--------+--------+---------+----+

A expressão regular que verifica a chave de acesso passa a suportar letras nas 12
primeiras posições do CNPJ::

    [0-9]{6}[A-Z0-9]{12}[0-9]{26}

.. note::
   Se algumas letras forem vedadas na composição do CNPJ Alfa, isso deve ser considerado
   também para a chave de acesso.

Cálculo do DV da Chave de Acesso
----------------------------------

O cálculo do DV da chave de acesso aplica a **mesma lógica do CNPJ Alfa**:

1. Substituir cada um dos 44 caracteres pelo valor ``código_ASCII - 48``.
2. Aplicar o cálculo do **módulo 11** sobre a totalidade dos dígitos resultantes
   (mesma lógica já utilizada para chaves puramente numéricas).

.. important::
   As rotinas de validação de chave de acesso devem rejeitar chaves contendo CNPJ
   Alfanuméricos informados **anteriores à data de implantação** de cada ambiente.
   A rejeição aplicada será a de falha no CNPJ informado na chave de acesso.

Código de Barras dos Documentos Auxiliares
==========================================

O padrão de código de barras impresso no documento auxiliar (DACTE, DANFE, DABPE, etc.)
é o **CODE-128C**, que suporta somente números. Por isso, ele **não é compatível** com
chaves de acesso que contenham caracteres alfanuméricos nas posições do CNPJ.

Novo Padrão Híbrido CODE-128A/C
---------------------------------

Para suportar o CNPJ Alfa, adota-se um **modelo híbrido**:

* **CODE-128C**: codifica pares de dígitos numéricos (00–99), usado nas partes numéricas.
* **CODE-128A**: aceita números e letras maiúsculas (ASCII 00–95), ativado na ocorrência
  de caracteres não numéricos.
* A alternância entre os modos é feita com o código ``100`` (CODE A ↔ CODE C).

Dimensões mínimas
-----------------

+---------------------------------+-------------------------------------+
| Tipo de impressora              | Largura mínima do código de barras  |
+=================================+=====================================+
| Não impacto (laser / jato de    | 11,5 cm                             |
| tinta)                          |                                     |
+---------------------------------+-------------------------------------+
| Impacto (matricial / de linha)  | 11,5 cm                             |
+---------------------------------+-------------------------------------+

* **Altura mínima da barra:** 0,8 cm
* **Largura mínima da barra:** 0,02 cm

.. note::
   Por conta da mudança para o CNPJ Alfa, o novo padrão híbrido (128-A + 128-C) poderá
   apresentar maior volume de dados para suportar os caracteres não numéricos, exigindo
   mais espaço para acomodar as barras adicionais.

Cálculo do Dígito Verificador do CODE-128
------------------------------------------

O DV do código de barras é baseado no **módulo 103**, calculado pela soma ponderada dos
valores de cada símbolo, incluindo o caractere de início (Start).

* O **Code-128C** usa ``105`` como Start.
* O **Code-128A** usa ``103`` como Start.

Algoritmo::

    DV = soma_ponderada % 103

Orientações para alternância entre CODE-128C e CODE-128A
---------------------------------------------------------

1. **Inicie** com o conjunto ``C`` (pois a chave começa com quatro ou mais dígitos).
2. Se os dados iniciam com número **ímpar** de dígitos: insira ``Code A`` antes do último
   dígito ímpar.
3. Se **4 ou mais dígitos** aparecerem em sequência enquanto no modo ``A``:

   * Par de dígitos → insira ``Code C`` antes do primeiro dígito.
   * Ímpar de dígitos → insira ``Code C`` após o primeiro dígito (o primeiro permanece em ``A``).

4. Quando **no modo C** e um caractere não numérico ocorrer: insira ``Code A`` antes do
   caractere não numérico.

Exemplo de Validação — CNPJ Alfa (JavaScript)
=============================================

O exemplo abaixo implementa a validação do CNPJ Alfa conforme a NT 2025.001:

.. code-block:: javascript

   class CNPJ {
     static tamanhoCNPJSemDV = 12;
     static regexCNPJSemDV = /^([A-Z\d]){12}$/;
     static regexCNPJ = /^([A-Z\d]){12}(\d){2}$/;
     static regexCaracteresMascara = /[./-]/g;
     static regexCaracteresNaoPermitidos = /[^A-Z\d./-]/i;
     static valorBase = "0".charCodeAt(0);
     static pesosDV = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];
     static cnpjZerado = "00000000000000";

     static isValid(cnpj) {
       if (!this.regexCaracteresNaoPermitidos.test(cnpj)) {
         let cnpjSemMascara = this.removeMascaraCNPJ(cnpj);
         if (this.regexCNPJ.test(cnpjSemMascara) && cnpjSemMascara !== this.cnpjZerado) {
           const dvInformado = cnpjSemMascara.substring(this.tamanhoCNPJSemDV);
           const dvCalculado = this.calculaDV(cnpjSemMascara.substring(0, this.tamanhoCNPJSemDV));
           return dvInformado === dvCalculado;
         }
       }
       return false;
     }

     static calculaDV(cnpj) {
       if (!this.regexCaracteresNaoPermitidos.test(cnpj)) {
         let cnpjSemMascara = this.removeMascaraCNPJ(cnpj);
         if (this.regexCNPJSemDV.test(cnpjSemMascara)
             && cnpjSemMascara !== this.cnpjZerado.substring(0, this.tamanhoCNPJSemDV)) {
           let somatorioDV1 = 0;
           let somatorioDV2 = 0;
           for (let i = 0; i < this.tamanhoCNPJSemDV; i++) {
             const asciiDigito = cnpjSemMascara.charCodeAt(i) - this.valorBase;
             somatorioDV1 += asciiDigito * this.pesosDV[i + 1];
             somatorioDV2 += asciiDigito * this.pesosDV[i];
           }
           const dv1 = somatorioDV1 % 11 < 2 ? 0 : 11 - (somatorioDV1 % 11);
           somatorioDV2 += dv1 * this.pesosDV[this.tamanhoCNPJSemDV];
           const dv2 = somatorioDV2 % 11 < 2 ? 0 : 11 - (somatorioDV2 % 11);
           return `${dv1}${dv2}`;
         }
       }
       throw new Error("Não é possível calcular o DV pois o CNPJ fornecido é inválido");
     }

     static removeMascaraCNPJ(cnpj) {
       return cnpj.replace(this.regexCaracteresMascara, "");
     }
   }

Exemplo de Validação — Chave de Acesso (Visual Basic .NET)
==========================================================

.. code-block:: vbnet

   Public Class ChaveAcesso
       Private Const TamanhoChaveAcessoSemDV = 43

       Public Shared Function ValidaDigitoChaveAcesso(ByVal chaveAcesso As String) As Boolean
           Dim digito As Char = CalculaDigitoVerificadorChaveAcesso(chaveAcesso).ToString()
           If digito <> chaveAcesso.Substring(43, 1) Then
               Return False
           Else
               Return True
           End If
       End Function

       Public Shared Function CalculaDigitoVerificadorChaveAcesso(chaveAcesso As String) As Integer
           ' Converte a string em um array de bytes com valor ASCII - 48
           Dim chAcessoBytes(TamanhoChaveAcessoSemDV - 1) As Byte
           For i As Integer = 0 To TamanhoChaveAcessoSemDV - 1
               chAcessoBytes(i) = CByte(Asc(chaveAcesso(i)) - 48)
           Next

           Dim soma As Integer = 0
           Dim peso As Integer = 2  ' multiplicador vai de 9 a 2

           ' Começa do final
           For i As Integer = TamanhoChaveAcessoSemDV - 1 To 0 Step -1
               soma = soma + Convert.ToInt32(chAcessoBytes(i)) * peso
               peso += 1
               If peso > 9 Then peso = 2
           Next

           Dim dv As Integer = 11 - (soma Mod 11)
           If dv >= 10 Then
               dv = 0
           End If

           Return dv
       End Function
   End Class

Referência
==========

* **Instrução Normativa RFB nº 2229**, de 15 de outubro de 2024 — modifica a regra de
  formação do CNPJ no Brasil.
* **Nota Técnica Conjunta 2025.001 v1.00** (25 de abril de 2025) — especificação do
  CNPJ Alfanumérico para DFe sob coordenação do ENCAT.
