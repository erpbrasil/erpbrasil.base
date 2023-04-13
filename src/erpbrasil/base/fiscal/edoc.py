# Copyright (C) 2015  Base4 Sistemas Ltda ME
# Copyright (C) 2020  Luis Felipe Mileo - KMEE
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import re

from ..misc import modulo11
from ..misc import punctuation_rm
from . import cnpj_cpf

ESTADOS_IBGE = {
    11: ["RO", "Rondônia"],
    12: ["AC", "Acre"],
    13: ["AM", "Amazonas"],
    14: ["RR", "Roraima"],
    15: ["PA", "Pará"],
    16: ["AP", "Amapá"],
    17: ["TO", "Tocantins"],
    21: ["MA", "Maranhão"],
    22: ["PI", "Piauí"],
    23: ["CE", "Ceará"],
    24: ["RN", "Rio Grande do Norte"],
    25: ["PB", "Paraíba"],
    26: ["PE", "Pernambuco"],
    27: ["AL", "Alagoas"],
    28: ["SE", "Sergipe"],
    29: ["BA", "Bahia"],
    31: ["MG", "Minas Gerais"],
    32: ["ES", "Espírito Santo"],
    33: ["RJ", "Rio de Janeiro"],
    35: ["SP", "São Paulo"],
    41: ["PR", "Paraná"],
    42: ["SC", "Santa Catarina"],
    43: ["RS", "Rio Grande do Sul"],
    50: ["MS", "Mato Grosso do Sul"],
    51: ["MT", "Mato Grosso"],
    52: ["GO", "Goiás"],
    53: ["DF", "Distrito Federal"],
}

CODIGO_ESTADOS_IBGE = list(ESTADOS_IBGE.keys())

EDOC_PREFIX = {
    "55": "NFe",
    "57": "CTe",
    "58": "MDFe",
    "59": "CFe",
    "65": "NFe",
}

CODIGO_MODELOS_EDOC = list(EDOC_PREFIX.keys())

CHAVE_REGEX = re.compile(r"(?P<campos>\d{44})$")


def detectar_chave_edoc(chave):
    """Converte a chave em texto no objeto correto"""
    matcher = CHAVE_REGEX.match(chave)
    if matcher:
        campos = matcher.group("campos")
    else:
        campos = False
    if not matcher and not campos:
        raise ValueError("Chave de acesso invalida: {!r}".format(chave))

    prefixo = EDOC_PREFIX.get(campos[20:22])

    if prefixo in ("NFe", "CTe", "MDFe"):
        return ChaveEdoc(chave=chave, validar=True)
    elif prefixo == "CFe":
        return ChaveCFeSAT(chave=chave, validar=True)
    raise ValueError("Chave de acesso invalida: {!r}".format(chave))


class ChaveEdoc(object):
    """
    Inspired on

    https://github.com/base4sistemas/satcomum/blob/f45da5b100a63511b9c455cbd6895b630e121866/satcomum/ersat.py


             0  2    6             20  22  25        34 35      43  --> índice
             |  |    |              |  |   |         | |        |
        MDFe 50 1312 48740351011795 58 000 149000153 1 16261964 8
             |  |    |              |  |   |         | |        |
        CTe  32 1712 32438772000104 57 001 000199075 1 39868226 3
             |  |    |              |  |   |         | |        |
        NFe  43 1402 01098983010680 65 796 000000599 1 31447746 1 #NFC-e
             |  |    |              |  |   |         | |        |
        NFe  35 2103 20695448000184 55 001 000003589 1 98183992 3
    """

    CUF = slice(0, 2)
    AAMM = slice(2, 6)
    CNPJ_CPF = slice(6, 20)
    MODELO = slice(20, 22)
    SERIE = slice(22, 25)
    NUMERO = slice(25, 34)
    FORMA = slice(34, 35)
    CODIGO = slice(35, 43)
    DV = slice(43, None)

    def __init__(
        self,
        chave=False,
        codigo_uf=False,
        ano_mes=False,
        cnpj_cpf_emitente=False,
        modelo_documento=False,
        numero_serie=False,
        numero_documento=False,
        forma_emissao=1,
        codigo_aleatorio=False,
        validar=False,
    ):
        if not chave:
            if not (
                codigo_uf
                and ano_mes
                and cnpj_cpf_emitente
                and modelo_documento
                and numero_documento
                and numero_documento
            ):
                raise ValueError("Impossível gerar a chave!!")

            campos = str(codigo_uf).zfill(self.CUF.stop - self.CUF.start)

            campos += ano_mes

            campos += str(punctuation_rm(cnpj_cpf_emitente)).zfill(
                self.CNPJ_CPF.stop - self.CNPJ_CPF.start
            )
            campos += str(modelo_documento).zfill(self.MODELO.stop - self.MODELO.start)
            campos += str(numero_serie).zfill(self.SERIE.stop - self.SERIE.start)
            campos += str(numero_documento).zfill(self.NUMERO.stop - self.NUMERO.start)

            #
            # A inclusão do tipo de emissão na chave já torna a chave válida
            # também para a versão 2.00 da NF-e
            #
            campos += str(forma_emissao).zfill(self.FORMA.stop - self.FORMA.start)

            if not codigo_aleatorio:
                codigo_aleatorio = self.calculo_codigo_aleatorio(campos)

            campos += str(codigo_aleatorio).zfill(self.CODIGO.stop - self.CODIGO.start)
            campos += str(modulo11(campos))
        else:
            matcher = CHAVE_REGEX.match(chave)
            if matcher:
                campos = matcher.group("campos")
            if not matcher or not campos:
                raise ValueError("Chave de acesso invalida: {!r}".format(chave))

        self.campos = campos
        self.prefixo = EDOC_PREFIX.get(self.modelo_documento, "")
        self.chave = self.campos

        if validar:
            self.validar()

    def calculo_codigo_aleatorio(self, campos):
        #
        # O código numério é um número aleatório
        #
        # chave += str(random.randint(0, 99999999)).strip().rjust(8, '0')

        #
        # Mas, por segurança, é preferível que esse número não seja
        # aleatório
        #
        soma = 0
        for c in campos:
            soma += int(c) ** 3**2

        TAMANHO_CODIGO = self.CODIGO.stop - self.CODIGO.start

        codigo = str(soma)
        if len(codigo) > TAMANHO_CODIGO:
            codigo = codigo[-TAMANHO_CODIGO:]
        else:
            codigo = codigo.rjust(TAMANHO_CODIGO, "0")
        return codigo

    def validar(self):
        """Validação da chave do documento fiscal


        cUF

        MODELO

        SERIE

        |Emit     |Processo Emissão       |Série   |Ch Acesso
        |CNPJ     |Aplicativo da Empresa  |000-889 |CNPJ do Emitente
        |CNPJ     |Programa Emissor Fisco |000-889 |CNPJ do Emitente
        |CNPJ/CPF |Site SEFAZ (NFA-e)     |890-899 |CNPJ da SEFAZ
        |CNPJ     |Site SEFAZ             |900-909 |CNPJ do Emitente
        |CPF      |Site SEFAZ             |910-919 |CPF do Emitente
        |CPF      |Aplicativo da Empresa  |920-969 |CPF do Emitente

        """

        # Verifica se o valor do campo CUF é válido
        # O valor deve ser o código do IBGE da UF
        if int(self.campos[ChaveEdoc.CUF]) not in CODIGO_ESTADOS_IBGE:
            raise ValueError(
                ("Chave de acesso invalida (codigo UF: {!r}): {!r}").format(
                    self.campos[ChaveEdoc.CUF], self.chave
                )
            )

        # Verifica se o valor do campo MODELO é válido
        if self.campos[ChaveEdoc.MODELO] not in CODIGO_MODELOS_EDOC:
            raise ValueError(
                (
                    "Chave de acesso invalida " "(Modelos não permitidos: {!r}): {!r}"
                ).format(self.campos[ChaveEdoc.MODELO], self.chave)
            )

        # Verifica se o valor do campo Série é válido
        series_cnpj = list(range(0, 889 + 1)) + list(range(900, 909 + 1))
        series_cnpj_cpf = list(range(890, 899 + 1))
        series_cpf = list(range(910, 969 + 1))
        series_geral = series_cnpj + series_cnpj_cpf + series_cpf

        serie_number = int(self.campos[ChaveEdoc.SERIE])
        if serie_number not in series_geral:
            raise ValueError(
                ("Chave de acesso invalida " "(Série: {!r}): {!r}").format(
                    self.campos[ChaveEdoc.SERIE], self.chave
                )
            )

        # Por padrão o documento do emitente é o CNPJ
        doc_emitente = ["CNPJ", self.campos[ChaveEdoc.CNPJ_CPF]]

        # Caso a série esteja entre 920 a 969, o documento do emitente
        # deve ser CPF
        # Caso a série esteja entre 890 e 899 o documento do emitente
        # pode ser CPF ou CNPJ
        if (serie_number in series_cpf) or (
            serie_number in series_cnpj_cpf
            and not cnpj_cpf.validar(self.campos[ChaveEdoc.CNPJ_CPF])
        ):
            doc_emitente = ["CPF", self.campos[ChaveEdoc.CNPJ_CPF][3:]]

        if not cnpj_cpf.validar(doc_emitente[1]):
            raise ValueError(
                ("Chave de acesso invalida " "({!r} emitente: {!r}): {!r}").format(
                    doc_emitente[0], cnpj_cpf.formata(doc_emitente[1]), self.chave
                )
            )

        digito = modulo11(self.campos[:43])
        if not (digito == int(self.campos[-1])):
            raise ValueError(
                (
                    "Digito verificador invalido: " "chave={!r}, digito calculado={!r}"
                ).format(self.chave, digito)
            )

    def __str__(self):
        return self.chaveMOD

    def __repr__(self):
        return "{:s}({!r})".format(self.__class__.__name__, self._chave)

    @property
    def chave(self):
        return self._chave

    @chave.setter
    def chave(self, value):
        self._chave = value

    @property
    def prefixo(self):
        return self._prefixo

    @prefixo.setter
    def prefixo(self, value):
        self._prefixo = value

    @property
    def prefixo_chave(self):
        return self._prefixo + self._chave

    @property
    def campos(self):
        return self._campos

    @campos.setter
    def campos(self, value):
        self._campos = value

    @property
    def codigo_uf(self):
        return int(self._campos[self.CUF])

    @property
    def ano_mes(self):
        return self._campos[self.AAMM]

    @property
    def ano_emissao(self):
        return int(self._campos[self.AAMM][:2]) + 2000

    @property
    def mes_emissao(self):
        return int(self._campos[self.AAMM][2:])

    @property
    def cnpj_cpf_emitente(self):
        return cnpj_cpf.formata(self._campos[self.CNPJ_CPF])

    @property
    def modelo_documento(self):
        return self._campos[self.MODELO]

    @property
    def numero_serie(self):
        return self._campos[self.SERIE]

    @property
    def numero_documento(self):
        return self._campos[self.NUMERO]

    @property
    def forma_emissao(self):
        return self._campos[self.FORMA]

    @property
    def codigo_aleatorio(self):
        return self._campos[self.CODIGO]

    @property
    def digito_verificador(self):
        return self._campos[self.DV]

    def partes(self, num_partes=11):
        assert 44 % num_partes == 0, (
            "O numero de partes nao produz um resultado inteiro (partes "
            "por 44 digitos): num_partes={!r}"
        ).format(num_partes)

        salto = 44 // num_partes
        return [self._campos[n: (n + salto)] for n in range(0, 44, salto)]


class ChaveCFeSAT(ChaveEdoc):
    CHAVE_REGEX = re.compile(r"^CFe(?P<campos>\d{44})$")

    SERIE = slice(22, 31)
    NUMERO = slice(31, 37)
    FORMA = slice(0, 0)
    CODIGO = slice(37, 43)  # CNF
    DV = slice(43, None)
