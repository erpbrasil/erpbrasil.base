# -*- coding: utf-8 -*-
#
# satcfe/constantes.py
#
# Copyright 2015 Base4 Sistemas Ltda ME
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

VERSAO_ER = '2.19.07'
"""Versão da Especificação de Requisitos (ER) do SAT-CF-e na qual esta
implementação se baseia.
"""

VERSAO_LAYOUT_ARQUIVO_DADOS_AC = '0.06'
"""Versão do layout do arquivo de dados enviado pelo Aplicativo Comercial."""

XML_DECL = '<?xml version="1.0" ?>'
"""Declaração de documento XML."""

XML_DECL_UNICODE = u'<?xml version="1.0" encoding="utf-8" ?>'
"""Declaração de documento XML incluindo a codificação de texto UTF-8."""

ROOT_TAG_VENDA = 'CFe'
"""Nome da tag raiz para documentos CF-e-SAT de venda."""

ROOT_TAG_CANCELAMENTO = 'CFeCanc'
"""Nome da tag raiz para documentos CF-e-SAT de cancelamento."""

ASSINATURA_AC_TESTE = 'SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT'
"""Assinatura do Aplicativo Comercial utilizada nos documentos de venda e
cancelamento realizados contra equipamentos SAT para desenvolvimento.
"""


STANDARD_C = 1
WINDOWS_STDCALL = 2

CONVENCOES_CHAMADA = (
        (STANDARD_C, u'Standard C'),
        (WINDOWS_STDCALL, u'Windows "stdcall"'),)


CERTIFICADO_ACSAT_SEFAZ = 1
CERTIFICADO_ICPBRASIL = 2
CERTIFICADO_ICPBRASIL_RENOVACAO = 3

TIPOS_CERTIFICADOS = (
        (CERTIFICADO_ACSAT_SEFAZ, u'AC-SAT/SEFAZ'),
        (CERTIFICADO_ICPBRASIL, u'ICP-Brasil'),
        (CERTIFICADO_ICPBRASIL_RENOVACAO, u'Renovação Certificado ICP-Brasil'),
    )


CODIGO_ATIVACAO_REGULAR = 1
CODIGO_ATIVACAO_EMERGENCIA = 2

TIPOS_CODIGOS_ATIVACAO = (
        (CODIGO_ATIVACAO_REGULAR, u'Código de Ativação Regular'),
        (CODIGO_ATIVACAO_EMERGENCIA, u'Código de Ativação de Emergência'),
    )


# tpAmb (B10), identificação do ambiente
B10_PRODUCAO = '1'
B10_TESTES = '2'

B10_TPAMB = (
        (B10_PRODUCAO, u'Produção'),
        (B10_TESTES, u'Testes'),
    )


# emit (C01), valores do elemento 'cRegTribISSQN' (C15)
C15_MICROEMPRESA_MUNICIPAL = '1'
C15_ESTIMATIVA = '2'
C15_SOCIEDADE_PROFISSIONAIS = '3'
C15_COOPERATIVA = '4'
C15_MICROEMPRESARIO_INDIVIDUAL = '5'

C15_CREGTRIBISSQN_EMIT = (
        (C15_MICROEMPRESA_MUNICIPAL, u'Microempresa Municipal'),
        (C15_ESTIMATIVA, u'Estimativa'),
        (C15_SOCIEDADE_PROFISSIONAIS, u'Sociedade de Profissionais'),
        (C15_COOPERATIVA, u'Cooperativa'),
        (C15_MICROEMPRESARIO_INDIVIDUAL, u'Microempresario Individual (MEI)'),
    )


# emit (C01), valores do elemento 'indRatISSQN' (C16)
C16_RATEADO = 'S'
C16_NAO_RATEADO = 'N'

C16_INDRATISSQN_EMIT = (
        (C16_RATEADO, u'Rateado'),
        (C16_NAO_RATEADO, u'Não Rateado'),
    )


I11_ARREDONDAMENTO = 'A'
I11_TRUNCAMENTO = 'T'

I11_INDREGRA = (
        (I11_ARREDONDAMENTO, u'Arredondamento'),
        (I11_TRUNCAMENTO, u'Truncamento'),)


N06_NACIONAL = '0'
N06_ESTRANGEIRA_IMPORTACAO_DIRETA = '1'
N06_ESTRANGEIRA_ADQUIRIDA_MERCADO_INTERNO = '2'
N06_NACIONAL_CONTEUDO_IMPORTADO_41_70_PORCENTO = '3'
N06_NACIONAL_PROCESSOS_PRODUTIVOS_BASICOS = '4'
N06_NACIONAL_CONTEUDO_IMPORTADO_MENOR_40_PORCENTO = '5'
N06_ESTRANGEIRA_IMPORTACAO_DIRETA_CAMEX = '6'
N06_ESTRANGEIRA_ADQUIRIDA_MERCADO_INTERNO_CAMEX = '7'
N06_NACIONAL_CONTEUDO_IMPORTADO_SUPERIOR_70_PORCENTO = '8'

N06_ORIG = (
        (N06_NACIONAL, u'Nacional'),
        (N06_ESTRANGEIRA_IMPORTACAO_DIRETA, u'Estrangeira, importação direta'),
        (N06_ESTRANGEIRA_ADQUIRIDA_MERCADO_INTERNO, u'Estrangeira, adquirida no mercado interno'),
        (N06_NACIONAL_CONTEUDO_IMPORTADO_41_70_PORCENTO, u'Nacional, conteúdo importado entre 41% e 70%'),
        (N06_NACIONAL_PROCESSOS_PRODUTIVOS_BASICOS, u'Nacional, produção conforme processos produtivos básicos'),
        (N06_NACIONAL_CONTEUDO_IMPORTADO_MENOR_40_PORCENTO, u'Nacional, conteúdo importado inferior ou igual a 40%'),
        (N06_ESTRANGEIRA_IMPORTACAO_DIRETA_CAMEX, u'Estrangeira, importação direta, sem similar nacional, constante na lista da CAMEX e gás natural'),
        (N06_ESTRANGEIRA_ADQUIRIDA_MERCADO_INTERNO_CAMEX, u'Estrangeira, adquirida no mercado interno, sem similar nacional, constante na lista da CAMEX e gás natural'),
        (N06_NACIONAL_CONTEUDO_IMPORTADO_SUPERIOR_70_PORCENTO, u'Nacional, conteúdo importado superior a 70%'),
    )


# ICMS00 (N02), valores do elemento 'CST' (N07)
N07_TRIBUTADA_INTEGRALMENTE = '00'
N07_TRIBUTADA_COM_REDUCAO_BC = '20'
N07_OUTROS = '90'

N07_CST_ICMS00 = (
        (N07_TRIBUTADA_INTEGRALMENTE, u'Tributada integralmente'),
        (N07_TRIBUTADA_COM_REDUCAO_BC, u'Tributada com redução na base de cálculo'),
        (N07_OUTROS, u'Outros'),
    )


# ICMS40 (N03), valores do elemento 'CST' (N07)
N07_ISENTO = '40'
N07_NAO_TRIBUTADO = '41'
N07_SUSPENSAO = '50'
N07_ICMS_COBRADO_ANTERIORMENTE_ST = '60'

N07_CST_ICMS40 = (
        (N07_ISENTO, u'Isento'),
        (N07_NAO_TRIBUTADO, u'Não tributado'),
        (N07_SUSPENSAO, u'Suspensão'),
        (N07_ICMS_COBRADO_ANTERIORMENTE_ST, u'ICMS cobrado anteriormente por Substituição Tributária'),
    )


# ICMSSN102 (N04), valores do elemento 'CSOSN' (N10)
N10_TRIBUTADA_SN_SEM_PERMISSAO_CREDITO = '102'
N10_IMUNE = '300'
N10_ICMS_COBRADO_ANTERIORMENTE_ST = '500'

N10_CSOSN_ICMSSN102 = (
        (N10_TRIBUTADA_SN_SEM_PERMISSAO_CREDITO, u'Tributada pelo Simples Nacional sem permissão de crédito'),
        (N10_IMUNE, u'Imune'),
        (N10_ICMS_COBRADO_ANTERIORMENTE_ST, u'ICMS cobrado anteriormente por Substituição Tributária'),
    )


# ICMSSN900 (N05), valores do elemento 'CSOSN' (N10)
N10_OUTROS = '900'

N10_CSOSN_ICMSSN900 = (
        (N10_OUTROS, u'Outros'),
    )


# PISAliq (Q02), valores do elemento 'CST' (Q07)
Q07_OP_TRIBUTAVEL_ALIQUOTA_NORMAL = '01'
Q07_OP_TRIBUTAVEL_ALIQUOTA_DIFERENCIADA = '02'
Q07_OP_TRIBUTAVEL_ST = '05'

Q07_CST_PISALIQ = (
        (Q07_OP_TRIBUTAVEL_ALIQUOTA_NORMAL, u'Operação tributável (alíquota normal)'),
        (Q07_OP_TRIBUTAVEL_ALIQUOTA_DIFERENCIADA, u'Operação tributável (aliquota diferenciada)'),
        (Q07_OP_TRIBUTAVEL_ST, u'Operação tributável por Substituição Tributária'),
    )


# PISQtde (Q03), valores do elemento 'CST' (Q07)
Q07_OP_TRIBUTAVEL_BC_QTD_VENDIDA_X_UN_PROD = '03'

Q07_CST_PISQTDE = (
        (Q07_OP_TRIBUTAVEL_BC_QTD_VENDIDA_X_UN_PROD,
                u'Operação tributável (BC = qtd. vendida X un. de produto)'),
    )


# PISNT (Q04), valores do elemento 'CST' (Q07)
Q07_OP_TRIBUTAVEL_MONOFASICA_ALIQUOTA_ZERO = '04'
Q07_OP_TRIBUTAVEL_ALIQUOTA_ZERO = '06'
Q07_OP_ISENTA_CONTRIBUICAO = '07'
Q07_OP_SEM_INCIDENCIA_CONTRIBUICAO = '08'
Q07_OP_COM_SUSPENSAO_CONTRIBUICAO = '09'

Q07_CST_PISNT = (
        (Q07_OP_TRIBUTAVEL_MONOFASICA_ALIQUOTA_ZERO, u'Operação tributável (monofásica, alíquota zero)'),
        (Q07_OP_TRIBUTAVEL_ALIQUOTA_ZERO, u'Operação tributável (alíquota zero)'),
        (Q07_OP_ISENTA_CONTRIBUICAO, u'Operação isenta da contribuição'),
        (Q07_OP_SEM_INCIDENCIA_CONTRIBUICAO, u'Operação sem incidência da contribuição'),
        (Q07_OP_COM_SUSPENSAO_CONTRIBUICAO, u'Operação com suspensão da contribuição'),
    )


# PISSN (Q05), valores do elemento 'CST' (Q07)
Q07_OUTRAS_OPERACOES_SAIDA = '49'

Q07_CST_PISSN = (
        (Q07_OUTRAS_OPERACOES_SAIDA, u'Outras operações de saída'),
    )


# PISOutr (Q06), valores do elemento 'CST' (Q07)
Q07_OUTRAS_OPERACOES = '99'

Q07_CST_PISOUTR = (
        (Q07_OUTRAS_OPERACOES, u'Outras operações'),
    )


# COFINSAliq (S02), valores do elemento 'CST' (S07)
S07_OP_TRIBUTAVEL_ALIQUOTA_NORMAL = '01'
S07_OP_TRIBUTAVEL_ALIQUOTA_DIFERENCIADA = '02'
S07_OP_TRIBUTAVEL_ST = '05'

S07_CST_COFINSALIQ = (
        (S07_OP_TRIBUTAVEL_ALIQUOTA_NORMAL, u'Operação tributável (alíquota normal)'),
        (S07_OP_TRIBUTAVEL_ALIQUOTA_DIFERENCIADA, u'Operação tributável (aliquota diferenciada)'),
        (S07_OP_TRIBUTAVEL_ST, u'Operação tributável por Substituição Tributária'),
    )


# COFINSQtde (S03), valores do elemento 'CST' (S07)
S07_OP_TRIBUTAVEL_BC_QTD_VENDIDA_X_UN_PROD = '03'

S07_CST_COFINSQTDE = (
        (S07_OP_TRIBUTAVEL_BC_QTD_VENDIDA_X_UN_PROD,
                u'Operação tributável (BC = qtd. vendida X un. de produto)'),
    )


# COFINSNT (S04), valores do elemento 'CST' (S07)
S07_OP_TRIBUTAVEL_MONOFASICA_ALIQUOTA_ZERO = '04'
S07_OP_TRIBUTAVEL_ALIQUOTA_ZERO = '06'
S07_OP_ISENTA_CONTRIBUICAO = '07'
S07_OP_SEM_INCIDENCIA_CONTRIBUICAO = '08'
S07_OP_COM_SUSPENSAO_CONTRIBUICAO = '09'

S07_CST_COFINSNT = (
        (S07_OP_TRIBUTAVEL_MONOFASICA_ALIQUOTA_ZERO, u'Operação tributável (monofásica, alíquota zero)'),
        (S07_OP_TRIBUTAVEL_ALIQUOTA_ZERO, u'Operação tributável (alíquota zero)'),
        (S07_OP_ISENTA_CONTRIBUICAO, u'Operação isenta da contribuição'),
        (S07_OP_SEM_INCIDENCIA_CONTRIBUICAO, u'Operação sem incidência da contribuição'),
        (S07_OP_COM_SUSPENSAO_CONTRIBUICAO, u'Operação com suspensão da contribuição'),
    )


# COFINSSN (S05), valores do elemento 'CST' (S07)
S07_OUTRAS_OPERACOES_SAIDA = '49'

S07_CST_COFINSSN = (
        (S07_OUTRAS_OPERACOES_SAIDA, u'Outras operações de saída'),
    )


# COFINSOutr (S06), valores do elemento 'CST' (S07)
S07_OUTRAS_OPERACOES = '99'

S07_CST_COFINSOUTR = (
        (S07_OUTRAS_OPERACOES, u'Outras operações'),
    )


# ISSQN (U01), valores do elemento 'cNatOp' (U09)
U09_TRIBUTACAO_MUNICIPIO = '01'
U09_TRIBUTACAO_FORA_MUNICIPIO = '02'
U09_ISENCAO = '03'
U09_IMUNE = '04'
U09_EXIGIBILIDADE_SUSPENSA_DECISAO_JUDICIAL = '05'
U09_EXIGIBILIDADE_SUSPENSA_PROC_ADM = '06'
U09_NAO_TRIBUTAVEL_OU_NAO_INCIDENTE = '07'
U09_EXPORTACAO_SERVICO = '08'

U09_CNATOP_ISSQN = (
        (U09_TRIBUTACAO_MUNICIPIO, u'Tributação no município'),
        (U09_TRIBUTACAO_FORA_MUNICIPIO, u'Tributação fora do município'),
        (U09_ISENCAO, u'Isenção'),
        (U09_IMUNE, u'Imune'),
        (U09_EXIGIBILIDADE_SUSPENSA_DECISAO_JUDICIAL, u'Exigibilidade suspensa por decisão judicial'),
        (U09_EXIGIBILIDADE_SUSPENSA_PROC_ADM, u'Exigibilidade suspensa por procedimento administrativo'),
        (U09_NAO_TRIBUTAVEL_OU_NAO_INCIDENTE, u'Não tributável ou não incidência'),
        (U09_EXPORTACAO_SERVICO, u'Exportação de serviço'),
    )


# ISSQN (U01), valores do elemento 'indIncFisc' (U10)
U10_SIM = '1'
U10_NAO = '2'

U10_INDINCFISC_ISSQN = (
        (U10_SIM, u'Sim'),
        (U10_NAO, u'Não'),
    )

# MP (WA02), valores do elemento 'cMP' (WA03)
WA03_DINHEIRO = '01'
WA03_CHEQUE = '02'
WA03_CARTAO_CREDITO = '03'
WA03_CARTAO_DEBITO = '04'
WA03_CREDITO_LOJA = '05'
WA03_VALE_ALIMENTACAO = '10'
WA03_VALE_REFEICAO = '11'
WA03_VALE_PRESENTE = '12'
WA03_VALE_COMBUSTIVEL = '13'
WA03_OUTROS = '99'

WA03_CMP_MP = (
        (WA03_DINHEIRO, u'Dinheiro'),
        (WA03_CHEQUE, u'Cheque'),
        (WA03_CARTAO_CREDITO, u'Cartão Crédito'),
        (WA03_CARTAO_DEBITO, u'Cartão Débito'),
        (WA03_CREDITO_LOJA, u'Crédito Loja'),
        (WA03_VALE_ALIMENTACAO, u'Vale Alimentação'),
        (WA03_VALE_REFEICAO, u'Vale Refeição'),
        (WA03_VALE_PRESENTE, u'Vale Presente'),
        (WA03_VALE_COMBUSTIVEL, u'Vale Combustível'),
        (WA03_OUTROS, u'Outros'),
    )


# Anexo 3 - Tabela de Credenciadoras de Cartão de Crédito/Débito
CREDENCIADORAS_CARTAO = (
        # Código da credenciadora, CNPJ, Nome (conforme consta no Anexo 3)
        ('001', '03.106.213/0001-90', u'Administradora de Cartões Sicredi Ltda.'),
        ('002', '03.106.213/0002-71', u'Administradora de Cartões Sicredi Ltda.(filial RS)'),
        ('003', '60.419.645/0001-95', u'Banco American Express S/A - AMEX'),
        ('004', '62.421.979/0001-29', u'BANCO GE - CAPITAL'),
        ('005', '58.160.789/0001-28', u'BANCO SAFRA S/A'),
        ('006', '07.679.404/0001-00', u'BANCO TOPÁZIO S/A'),
        ('007', '17.351.180/0001-59', u'BANCO TRIANGULO S/A'),
        ('008', '04.627.085/0001-93', u'BIGCARD Adm. de Convenios e Serv.'),
        ('009', '01.418.852/0001-66', u'BOURBON Adm. de Cartões de Crédito'),
        ('010', '03.766.873/0001-06', u'CABAL Brasil Ltda.'),
        ('011', '03.722.919/0001-87', u'CETELEM Brasil S/A - CFI'),
        ('012', '01.027.058/0001-91', u'CIELO S/A'),
        ('013', '03.529.067/0001-06', u'CREDI 21 Participações Ltda.'),
        ('014', '71.225.700/0001-22', u'ECX CARD Adm. e Processadora de Cartões S/A'),
        ('015', '03.506.307/0001-57', u'Empresa Bras. Tec. Adm. Conv. Hom. Ltda. - EMBRATEC'),
        ('016', '04.432.048/0001-20', u'EMPÓRIO CARD LTDA'),
        ('017', '07.953.674/0001-50', u'FREEDDOM e Tecnologia e Serviços S/A'),
        ('018', '03.322.366/0001-75', u'FUNCIONAL CARD LTDA.'),
        ('019', '03.012.230/0001-69', u'HIPERCARD Banco Multiplo S/A'),
        ('020', '03.966.317/0001-75', u'MAPA Admin. Conv. e Cartões Ltda.'),
        ('021', '00.163.051/0001-34', u'Novo Pag Adm. e Proc. de Meios Eletrônicos de Pagto. Ltda.'),
        ('022', '43.180.355/0001-12', u'PERNAMBUCANAS Financiadora S/A Crédito, Fin. e Invest.'),
        ('023', '00.904.951/0001-95', u'POLICARD Systems e Serviços Ltda.'),
        ('024', '33.098.658/0001-37', u'PROVAR Negócios de Varejo Ltda.'),
        ('025', '01.425.787/0001-04', u'REDECARD S/A'),
        ('026', '90.055.609/0001-50', u'RENNER Adm. Cartões de Crédito Ltda.'),
        ('027', '03.007.699/0001-00', u'RP Administração de Convênios Ltda.'),
        ('028', '00.122.327/0001-36', u'SANTINVEST S/A Crédito, Financiamento e Investimentos'),
        ('029', '69.034.668/0001-56', u'SODEXHO Pass do Brasil Serviços e Comércio S/A'),
        ('030', '60.114.865/0001-00', u'SOROCRED Meios de Pagamentos Ltda.'),
        ('031', '51.427.102/0004-71', u'Tecnologia Bancária S/A - TECBAN'),
        ('032', '47.866.934/0001-74', u'TICKET Serviços S/A'),
        ('033', '00.604.122/0001-97', u'TRIVALE Administração Ltda.'),
        ('034', '61.071.387/0001-61', u'Unicard Banco Múltiplo S/A - TRICARD'),
        ('999', '0', u'Outros'),)


REDE_TIPOINTER_ETHE = 'ETHE'
REDE_TIPOINTER_WIFI = 'WIFI'

REDE_TIPOINTER_OPCOES = (
        (REDE_TIPOINTER_ETHE, u'Ethernet'),
        (REDE_TIPOINTER_WIFI, u'WiFi'),
    )


REDE_SEG_NONE = 'NONE'
REDE_SEG_WEP = 'WEP'
REDE_SEG_WPA_PERSONAL = 'WPA-PERSONAL'
REDE_SEG_WPA_ENTERPRISE = 'WPA-ENTERPRISE'

REDE_SEG_OPCOES = (
        (REDE_SEG_NONE, u'Nenhuma'),
        (REDE_SEG_WEP, u'WEP'),
        (REDE_SEG_WPA_PERSONAL, u'WPA Personal'),
        (REDE_SEG_WPA_ENTERPRISE, u'WPA Enterprise'),
    )


REDE_TIPOLAN_DHCP = 'DHCP'
REDE_TIPOLAN_PPPOE = 'PPPOE'
REDE_TIPOLAN_IPFIX = 'IPFIX'

REDE_TIPOLAN_OPCOES = (
        (REDE_TIPOLAN_DHCP, u'DHCP'),
        (REDE_TIPOLAN_PPPOE, u'PPPoE'),
        (REDE_TIPOLAN_IPFIX, u'IP fixo'),
    )


REDE_PROXY_NONE = '0'
REDE_PROXY_CONFIGURACAO = '1'
REDE_PROXY_TRANSPARENTE = '2'

REDE_PROXY_OPCOES = (
        (REDE_PROXY_NONE, u'Sem Proxy'),
        (REDE_PROXY_CONFIGURACAO, u'Proxy com configuração'),
        (REDE_PROXY_TRANSPARENTE, u'Proxy transparente'),
    )
