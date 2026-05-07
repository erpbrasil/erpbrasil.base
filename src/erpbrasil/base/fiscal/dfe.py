# Copyright (C) 2015  Base4 Sistemas Ltda ME
# Copyright (C) 2020  Luis Felipe Mileo - KMEE
# Copyright (C) 2024  Renato Lima
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

"""Módulo DFe: geração e validação de chaves de acesso dos Documentos Fiscais
Eletrônicos (DFe) brasileiros.

Documentos suportados:
    - NF-e  (mod 55)
    - NFC-e (mod 65)
    - CT-e  (mod 57)
    - MDF-e (mod 58)
    - CF-e SAT (mod 59) — via ChaveCFeSAT
    - NFCom (mod 62)
    - BP-e  (mod 63)
    - NF3e  (mod 66)
    - NFAg  (mod 75)
    - NFGas (mod 76)

Nomenclatura dos campos:
    Os campos seguem os nomes oficiais do schema XML da SEFAZ (NT 2018.001):
        cUF    — Código da UF do emitente (2 dígitos)
        dhEmi  — Ano e Mês de emissão, formato AAMM (4 dígitos)
        CNPJ   — CNPJ do emitente (14 dígitos)
        CPF    — CPF do emitente, quando aplicável (11 dígitos, precedido de zeros)
        mod    — Modelo do documento fiscal (2 dígitos)
        serie  — Série do documento fiscal (3 dígitos)
        nNF    — Número do documento fiscal (9 dígitos)
        tpEmis — Forma de emissão (1 dígito)
        cNF    — Código numérico aleatório (8 ou 7 dígitos, dependendo do modelo)
        cDV    — Dígito verificador (1 dígito)
        procEmi — Processo de emissão (campo XML id:B26, não faz parte da chave)

    Propriedades legadas mantidas para retrocompatibilidade:
        codigo_uf        → cUF
        ano_mes          → dhEmi
        cnpj_cpf_emitente
        modelo_documento → mod
        numero_serie     → serie
        numero_documento → nNF
        forma_emissao    → tpEmis
        codigo_aleatorio → cNF
        digito_verificador → cDV
"""

import re

from ..misc import modulo11
from ..misc import punctuation_rm
from . import cnpj_cpf

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

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
    "62": "NFCom",
    "63": "BPe",
    "65": "NFe",
    "66": "NF3e",
    "75": "NFAg",
    "76": "NFGas",
}

CODIGO_MODELOS_EDOC = list(EDOC_PREFIX.keys())

CHAVE_REGEX = re.compile(r"(?P<campos>\d{44})$")

# Regex para chave de acesso da NFS-e (50 dígitos numéricos)
# Estrutura: cMun(7) ambGer(1) tpInsc(1) CNPJ/CPF(14) nNFSe(13) AAMM(4) cNF(9) cDV(1) = 50
CHAVE_NFSE_REGEX = re.compile(r"(?P<campos>\d{50})$")

# Tipo de inscrição federal do emitente da NFS-e
TP_INSC_NFSE = {
    "1": "CPF",
    "2": "CNPJ",
}

# Modelos que incluem o campo nSiteAutoriz na chave (1 dígito extra antes de cNF)
MODELOS_SITE_AUTORIZ = ("62", "66", "75", "76")

# Processo de emissão do DFe (campo procEmi, id:B26 no schema XML da NF-e).
# Não compõe a chave de acesso, mas determina as faixas de série permitidas
# e é obrigatório no XML transmitido à SEFAZ.
PROC_EMI = {
    0: "Emissão de NF-e com aplicativo do contribuinte",
    1: "Emissão de NF-e avulsa pelo Fisco",
    2: "Emissão de NF-e avulsa pelo contribuinte com certificado digital via site do Fisco",
    3: "Emissão de NF-e pelo contribuinte com aplicativo fornecido pelo Fisco",
}

# Mapeamento de procEmi → faixas de série válidas para NF-e/NFC-e (mod 55/65).
# Fonte: NT 2018.001 e Manual de Orientação do Contribuinte.
PROC_EMI_SERIES = {
    0: list(range(0, 890)) + list(range(920, 970)),   # app do contribuinte
    1: list(range(890, 900)),                           # avulsa pelo Fisco (NFA-e)
    2: list(range(900, 920)),                           # site do Fisco (CNPJ 900-909 / CPF 910-919)
    3: list(range(0, 890)),                             # app fornecido pelo Fisco
}


# ---------------------------------------------------------------------------
# Função auxiliar
# ---------------------------------------------------------------------------

def detectar_chave_dfe(chave):
    """Detecta o tipo de DFe pela chave de acesso e retorna o objeto correto.

    Suporta chaves de 44 dígitos (DFe padrão e CF-e SAT) e 50 dígitos (NFS-e).

    Args:
        chave (str): Chave de acesso numérica (44 ou 50 dígitos).

    Returns:
        ChaveDFe | ChaveCFeSAT | ChaveNFSe: Instância validada do documento fiscal.

    Raises:
        ValueError: Se a chave for inválida ou o modelo não for reconhecido.
    """
    # Tenta NFS-e primeiro (50 dígitos)
    matcher_nfse = CHAVE_NFSE_REGEX.match(chave)
    if matcher_nfse:
        return ChaveNFSe(chave=chave, validar=True)

    matcher = CHAVE_REGEX.match(chave)
    if matcher:
        campos = matcher.group("campos")
    else:
        campos = False
    if not matcher and not campos:
        raise ValueError("Chave de acesso invalida: {!r}".format(chave))

    prefixo = EDOC_PREFIX.get(campos[20:22])

    if prefixo in ("NFe", "CTe", "MDFe", "NFCom", "BPe", "NF3e", "NFAg", "NFGas"):
        return ChaveDFe(chave=chave, validar=True)
    elif prefixo == "CFe":
        return ChaveCFeSAT(chave=chave, validar=True)
    raise ValueError("Chave de acesso invalida: {!r}".format(chave))


# ---------------------------------------------------------------------------
# Classe principal
# ---------------------------------------------------------------------------

class ChaveDFe:
    """Chave de acesso dos Documentos Fiscais Eletrônicos (DFe).

    Permite gerar uma chave a partir dos campos individuais ou decompor uma
    chave existente nos seus campos, além de validar a integridade da chave.

    Estrutura da chave (44 dígitos):

         0  2    6             20  22  25        34 35      43  --> índice
         |  |    |              |  |   |         | |        |
    MDFe 50 1312 48740351011795 58 000 149000153 1 16261964 8
         |  |    |              |  |   |         | |        |
    CTe  32 1712 32438772000104 57 001 000199075 1 39868226 3
         |  |    |              |  |   |         | |        |
    NFe  43 1402 01098983010680 65 796 000000599 1 31447746 1 #NFC-e
         |  |    |              |  |   |         | |        |
    NFe  35 2103 20695448000184 55 001 000003589 1 98183992 3

    Para modelos com site autorizador (NF3e=66, NFCom=62, NFAg=75, NFGas=76):

         0  2    6             20  22  25        34 35 36      43  --> índice
         |  |    |              |  |   |         |  |  |        |
    NF3e 35 2401 02960895000131 66 001 123456789 1  2  1234567  X
                                                    ^-- nSiteAutoriz (1 dígito)
                                                       ^-- cNF (7 dígitos)

    Nomenclatura dos campos (nomes oficiais do schema XML):
        cUF    (slice 0:2)  — Código IBGE da UF do emitente
        dhEmi  (slice 2:6)  — AAMM de emissão
        CNPJ   (slice 6:20) — CNPJ/CPF do emitente (14 posições)
        mod    (slice 20:22)— Modelo do documento
        serie  (slice 22:25)— Série do documento
        nNF    (slice 25:34)— Número do documento
        tpEmis (slice 34:35)— Forma de emissão
        cNF    (slice 35:43 ou 36:43 para site_autoriz) — Código numérico
        cDV    (slice 43:44)— Dígito verificador
    """

    # Slices para acesso aos campos da chave (posições 0-based, 44 dígitos total)
    CUF = slice(0, 2)
    AAMM = slice(2, 6)
    CNPJ_CPF = slice(6, 20)
    MODELO = slice(20, 22)
    SERIE = slice(22, 25)
    NUMERO = slice(25, 34)
    FORMA = slice(34, 35)
    SITE_AUTORIZ = slice(35, 36)   # nSiteAutoriz — apenas modelos MODELOS_SITE_AUTORIZ
    CODIGO = slice(35, 43)         # cNF padrão (8 dígitos)
    CODIGO_SITE = slice(36, 43)    # cNF para modelos com site_autoriz (7 dígitos)
    DV = slice(43, None)

    def __init__(
        self,
        chave=False,
        # Nomes oficiais XML
        cUF=False,
        dhEmi=False,
        CNPJ=False,
        CPF=False,
        mod=False,
        serie=False,
        nNF=False,
        tpEmis=1,
        nSiteAutoriz=False,
        cNF=False,
        procEmi=None,
        # Nomes legados (retrocompatibilidade)
        codigo_uf=False,
        ano_mes=False,
        cnpj_cpf_emitente=False,
        modelo_documento=False,
        numero_serie=False,
        numero_documento=False,
        forma_emissao=False,
        site_autorizador=False,
        codigo_aleatorio=False,
        validar=False,
    ):
        """Inicializa a chave DFe a partir de uma chave completa ou de campos individuais.

        Aceita tanto os nomes oficiais do schema XML quanto os nomes legados.
        Em caso de conflito, os nomes oficiais têm precedência.

        Args:
            chave (str, optional): Chave de acesso completa com 44 dígitos.
            cUF (int, optional): Código IBGE da UF do emitente. Alias: codigo_uf.
            dhEmi (str, optional): Ano e mês de emissão no formato AAMM. Alias: ano_mes.
            CNPJ (str, optional): CNPJ do emitente (com ou sem pontuação).
            CPF (str, optional): CPF do emitente (com ou sem pontuação), precedido de zeros.
            mod (str, optional): Modelo do documento fiscal. Alias: modelo_documento.
            serie (str, optional): Série do documento. Alias: numero_serie.
            nNF (str, optional): Número do documento. Alias: numero_documento.
            tpEmis (int, optional): Forma de emissão (padrão 1). Alias: forma_emissao.
            nSiteAutoriz (str, optional): Site autorizador (apenas modelos específicos).
                Alias: site_autorizador.
            cNF (str, optional): Código numérico aleatório. Alias: codigo_aleatorio.
            procEmi (int, optional): Processo de emissão (campo XML id:B26). Não faz
                parte da chave de acesso, mas é armazenado para validação cruzada com
                a série e para preenchimento do XML. Valores válidos: 0, 1, 2, 3.
                Se informado junto com ``validar=True``, valida a combinação
                procEmi × serie (Rejeição 266 da SEFAZ).
            validar (bool, optional): Se True, valida a chave após a geração/parse.

        Raises:
            ValueError: Se os campos obrigatórios não forem informados ou a chave
                for inválida.
        """
        # Resolve nomes oficiais vs legados (oficiais têm precedência)
        _codigo_uf = cUF or codigo_uf
        _ano_mes = dhEmi or ano_mes
        _cnpj_cpf = CNPJ or CPF or cnpj_cpf_emitente
        _modelo = mod or modelo_documento
        _serie = serie or numero_serie
        _numero = nNF or numero_documento
        _forma = tpEmis if tpEmis != 1 else (forma_emissao if forma_emissao else 1)
        # tpEmis default é 1; se forma_emissao foi passado, usa ele quando tpEmis==1
        if tpEmis == 1 and forma_emissao:
            _forma = forma_emissao
        else:
            _forma = tpEmis
        _site = nSiteAutoriz or site_autorizador
        _codigo_aleatorio = cNF or codigo_aleatorio

        if not chave:
            if not (_codigo_uf and _ano_mes and _cnpj_cpf and _modelo and _numero and _serie):
                raise ValueError("Impossível gerar a chave!!")

            campos = str(_codigo_uf).zfill(self.CUF.stop - self.CUF.start)
            campos += _ano_mes
            campos += str(punctuation_rm(_cnpj_cpf)).zfill(
                self.CNPJ_CPF.stop - self.CNPJ_CPF.start
            )
            campos += str(_modelo).zfill(self.MODELO.stop - self.MODELO.start)
            campos += str(_serie).zfill(self.SERIE.stop - self.SERIE.start)
            campos += str(_numero).zfill(self.NUMERO.stop - self.NUMERO.start)

            # A inclusão do tpEmis na chave torna a chave válida para NF-e v2.00+
            campos += str(_forma).zfill(self.FORMA.stop - self.FORMA.start)

            if str(_modelo) in MODELOS_SITE_AUTORIZ:
                campos += str(_site or 0).zfill(
                    self.SITE_AUTORIZ.stop - self.SITE_AUTORIZ.start
                )

            if not _codigo_aleatorio:
                _codigo_aleatorio = self.calculo_codigo_aleatorio(campos, _modelo)

            if str(_modelo) in MODELOS_SITE_AUTORIZ:
                campos += str(_codigo_aleatorio).zfill(
                    self.CODIGO_SITE.stop - self.CODIGO_SITE.start
                )
            else:
                campos += str(_codigo_aleatorio).zfill(
                    self.CODIGO.stop - self.CODIGO.start
                )
            campos += str(modulo11(campos))
        else:
            matcher = CHAVE_REGEX.match(chave)
            if matcher:
                campos = matcher.group("campos")
            if not matcher or not campos:
                raise ValueError("Chave de acesso invalida: {!r}".format(chave))

        self.campos = campos
        self.prefixo = EDOC_PREFIX.get(self.mod, "")
        self.chave = self.campos
        self._proc_emi = procEmi

        if validar:
            self.validar()

    # -----------------------------------------------------------------------
    # Geração do código numérico aleatório
    # -----------------------------------------------------------------------

    def calculo_codigo_aleatorio(self, campos, modelo=False):
        """Calcula um código numérico determinístico baseado nos campos da chave.

        Por segurança, em vez de usar um número verdadeiramente aleatório, usa
        uma função determinística dos campos já montados.

        Args:
            campos (str): String parcial da chave (sem cNF e cDV).
            modelo (str, optional): Código do modelo do documento.

        Returns:
            str: Código numérico com o número de dígitos adequado ao modelo.
        """
        soma = 0
        for c in campos:
            soma += int(c) ** 3 ** 2

        if str(modelo) in MODELOS_SITE_AUTORIZ:
            tamanho = self.CODIGO_SITE.stop - self.CODIGO_SITE.start
        else:
            tamanho = self.CODIGO.stop - self.CODIGO.start

        codigo = str(soma)
        if len(codigo) > tamanho:
            codigo = codigo[-tamanho:]
        else:
            codigo = codigo.rjust(tamanho, "0")
        return codigo

    # -----------------------------------------------------------------------
    # Validação
    # -----------------------------------------------------------------------

    def validar(self):
        """Valida a chave de acesso do documento fiscal.

        Validações realizadas:
            - cUF: código IBGE válido
            - mod: modelo de documento reconhecido
            - serie: faixas reservadas (apenas NF-e/NFC-e)
            - CNPJ/CPF do emitente: dígitos verificadores válidos
            - nSiteAutoriz: apenas dígitos (modelos com site autorizador)
            - cDV: dígito verificador (módulo 11)
            - procEmi × serie: combinação válida (Rejeição 266), quando procEmi
              for informado e o modelo for NF-e/NFC-e (mod 55/65)

        Faixas de série (NF-e/NFC-e — mod 55 e 65):
            000–889 e 920–969 → procEmi 0 ou 3 (app do contribuinte / app do Fisco)
            890–899           → procEmi 1 (NFA-e avulsa pelo Fisco)
            900–919           → procEmi 2 (via site do Fisco — CNPJ 900-909 / CPF 910-919)

        Raises:
            ValueError: Se qualquer validação falhar, com mensagem descritiva.
        """
        # Verifica cUF
        if int(self.campos[ChaveDFe.CUF]) not in CODIGO_ESTADOS_IBGE:
            raise ValueError(
                ("Chave de acesso invalida (codigo UF: {!r}): {!r}").format(
                    self.campos[ChaveDFe.CUF], self.chave
                )
            )

        # Verifica mod
        if self.campos[ChaveDFe.MODELO] not in CODIGO_MODELOS_EDOC:
            raise ValueError(
                (
                    "Chave de acesso invalida "
                    "(Modelos não permitidos: {!r}): {!r}"
                ).format(self.campos[ChaveDFe.MODELO], self.chave)
            )

        # Verifica serie (específico para NF-e/NFC-e)
        series_cnpj = list(range(0, 889 + 1)) + list(range(900, 909 + 1))
        series_cnpj_cpf = list(range(890, 899 + 1))
        series_cpf = list(range(910, 969 + 1))
        series_geral = series_cnpj + series_cnpj_cpf + series_cpf

        serie_number = int(self.campos[ChaveDFe.SERIE])
        if self.mod in ("55", "65") and serie_number not in series_geral:
            raise ValueError(
                ("Chave de acesso invalida (Série: {!r}): {!r}").format(
                    self.campos[ChaveDFe.SERIE], self.chave
                )
            )

        # Verifica CNPJ/CPF do emitente
        doc_emitente = ["CNPJ", self.campos[ChaveDFe.CNPJ_CPF]]

        if self.mod in ("55", "65") and (
            (serie_number in series_cpf)
            or (
                serie_number in series_cnpj_cpf
                and not cnpj_cpf.validar(self.campos[ChaveDFe.CNPJ_CPF])
            )
        ):
            doc_emitente = ["CPF", self.campos[ChaveDFe.CNPJ_CPF][3:]]

        if not cnpj_cpf.validar(doc_emitente[1]):
            raise ValueError(
                ("Chave de acesso invalida ({!r} emitente: {!r}): {!r}").format(
                    doc_emitente[0], cnpj_cpf.formata(doc_emitente[1]), self.chave
                )
            )

        # Verifica nSiteAutoriz (apenas modelos específicos)
        if (
            self.mod in MODELOS_SITE_AUTORIZ
            and not self.campos[ChaveDFe.SITE_AUTORIZ].isdigit()
        ):
            raise ValueError(
                ("Chave de acesso invalida (Site Autorizador: {!r}): {!r}").format(
                    self.campos[ChaveDFe.SITE_AUTORIZ], self.chave
                )
            )

        # Verifica procEmi × serie (Rejeição 266) — apenas quando procEmi for informado
        if self._proc_emi is not None and self.mod in ("55", "65"):
            if self._proc_emi not in PROC_EMI:
                raise ValueError(
                    ("procEmi inválido ({!r}): valores permitidos são {}").format(
                        self._proc_emi, list(PROC_EMI.keys())
                    )
                )
            series_permitidas = PROC_EMI_SERIES[self._proc_emi]
            if serie_number not in series_permitidas:
                raise ValueError(
                    (
                        "Combinação inválida de procEmi e série (Rejeição 266): "
                        "procEmi={!r} não permite série {!r}"
                    ).format(self._proc_emi, self.campos[ChaveDFe.SERIE])
                )

        # Verifica cDV (módulo 11)
        digito = modulo11(self.campos[:43])
        if not (digito == int(self.campos[-1])):
            raise ValueError(
                (
                    "Digito verificador invalido: "
                    "chave={!r}, digito calculado={!r}"
                ).format(self.chave, digito)
            )

    # -----------------------------------------------------------------------
    # Representação
    # -----------------------------------------------------------------------

    def __str__(self):
        return self.chave

    def __repr__(self):
        return "{:s}({!r})".format(self.__class__.__name__, self._chave)

    # -----------------------------------------------------------------------
    # Propriedades — chave e prefixo
    # -----------------------------------------------------------------------

    @property
    def chave(self):
        """Chave de acesso completa (44 dígitos)."""
        return self._chave

    @chave.setter
    def chave(self, value):
        self._chave = value

    @property
    def dfe_key(self):
        """Alias oficial para a chave de acesso completa."""
        return self._chave

    @property
    def prefixo(self):
        """Prefixo textual do tipo de documento (ex: 'NFe', 'CTe')."""
        return self._prefixo

    @prefixo.setter
    def prefixo(self, value):
        self._prefixo = value

    @property
    def prefixo_chave(self):
        """Prefixo concatenado com a chave (ex: 'NFe35210320...')."""
        return self._prefixo + self._chave

    @property
    def campos(self):
        """String interna com os 44 dígitos da chave."""
        return self._campos

    @campos.setter
    def campos(self, value):
        self._campos = value

    # -----------------------------------------------------------------------
    # Propriedades — campos com nomes oficiais XML
    # -----------------------------------------------------------------------

    @property
    def cUF(self):
        """Código IBGE da UF do emitente (int)."""
        return int(self._campos[self.CUF])

    @property
    def dhEmi(self):
        """Ano e Mês de emissão no formato AAMM (str, 4 dígitos)."""
        return self._campos[self.AAMM]

    @property
    def mod(self):
        """Modelo do documento fiscal (str, 2 dígitos)."""
        return self._campos[self.MODELO]

    @property
    def serie(self):
        """Série do documento fiscal (str, 3 dígitos)."""
        return self._campos[self.SERIE]

    @property
    def nNF(self):
        """Número do documento fiscal (str, 9 dígitos)."""
        return self._campos[self.NUMERO]

    @property
    def tpEmis(self):
        """Forma de emissão (str, 1 dígito)."""
        return self._campos[self.FORMA]

    @property
    def nSiteAutoriz(self):
        """Site autorizador (str, 1 dígito) — apenas modelos com site autoriz.

        Returns:
            str | False: Dígito do site autorizador ou False se não aplicável.
        """
        if self.mod in MODELOS_SITE_AUTORIZ:
            return self._campos[self.SITE_AUTORIZ]
        return False

    @property
    def cNF(self):
        """Código numérico que compõe a chave de acesso (str, 7 ou 8 dígitos)."""
        if self.mod in MODELOS_SITE_AUTORIZ:
            return self._campos[self.CODIGO_SITE]
        return self._campos[self.CODIGO]

    @property
    def cDV(self):
        """Dígito verificador da chave de acesso (str, 1 dígito)."""
        return self._campos[self.DV]

    # -----------------------------------------------------------------------
    # Propriedades legadas (retrocompatibilidade com ChaveEdoc)
    # -----------------------------------------------------------------------

    @property
    def codigo_uf(self):
        """(Legado) Código IBGE da UF. Use ``cUF`` nas novas implementações."""
        return self.cUF

    @property
    def ano_mes(self):
        """(Legado) Ano e Mês AAMM. Use ``dhEmi`` nas novas implementações."""
        return self.dhEmi

    @property
    def ano_emissao(self):
        """Ano de emissão (int, ex: 2021)."""
        return int(self._campos[self.AAMM][:2]) + 2000

    @property
    def mes_emissao(self):
        """Mês de emissão (int, 1-12)."""
        return int(self._campos[self.AAMM][2:])

    @property
    def cnpj_cpf_emitente(self):
        """CNPJ ou CPF do emitente formatado."""
        return cnpj_cpf.formata(self._campos[self.CNPJ_CPF])

    @property
    def modelo_documento(self):
        """(Legado) Modelo do documento. Use ``mod`` nas novas implementações."""
        return self.mod

    @property
    def numero_serie(self):
        """(Legado) Série do documento. Use ``serie`` nas novas implementações."""
        return self.serie

    @property
    def numero_documento(self):
        """(Legado) Número do documento. Use ``nNF`` nas novas implementações."""
        return self.nNF

    @property
    def forma_emissao(self):
        """(Legado) Forma de emissão. Use ``tpEmis`` nas novas implementações."""
        return self.tpEmis

    @property
    def site_autorizador(self):
        """(Legado) Site autorizador. Use ``nSiteAutoriz`` nas novas implementações."""
        return self.nSiteAutoriz

    @property
    def codigo_aleatorio(self):
        """(Legado) Código numérico aleatório. Use ``cNF`` nas novas implementações."""
        return self.cNF

    @property
    def digito_verificador(self):
        """(Legado) Dígito verificador. Use ``cDV`` nas novas implementações."""
        return self.cDV

    @property
    def procEmi(self):
        """Processo de emissão do DFe (campo XML id:B26, não compõe a chave).

        Indica como o arquivo XML foi gerado:
            0 — Emissão com aplicativo do próprio contribuinte
            1 — Emissão avulsa pelo Fisco
            2 — Emissão avulsa pelo contribuinte via site do Fisco
            3 — Emissão com aplicativo fornecido pelo Fisco

        Returns:
            int | None: Valor informado no construtor, ou None se não informado.
        """
        return self._proc_emi

    @property
    def procEmi_descricao(self):
        """Descrição textual do processo de emissão.

        Returns:
            str | None: Descrição do procEmi, ou None se não informado.
        """
        if self._proc_emi is None:
            return None
        return PROC_EMI.get(self._proc_emi, "procEmi desconhecido: {!r}".format(self._proc_emi))

    # -----------------------------------------------------------------------
    # Utilidades
    # -----------------------------------------------------------------------

    def partes(self, num_partes=11):
        """Divide a chave em partes iguais para exibição.

        Args:
            num_partes (int): Número de partes. Deve dividir 44 exatamente.
                Padrão: 11 partes de 4 dígitos cada.

        Returns:
            list[str]: Lista com as partes da chave.

        Raises:
            AssertionError: Se ``num_partes`` não dividir 44 de forma exata.
        """
        assert 44 % num_partes == 0, (
            "O numero de partes nao produz um resultado inteiro (partes "
            "por 44 digitos): num_partes={!r}"
        ).format(num_partes)

        salto = 44 // num_partes
        return [self._campos[n : (n + salto)] for n in range(0, 44, salto)]


# ---------------------------------------------------------------------------
# Subclasse CF-e SAT
# ---------------------------------------------------------------------------

class ChaveCFeSAT(ChaveDFe):
    """Chave de acesso do CF-e SAT (modelo 59).

    O CF-e SAT possui uma estrutura de campos diferente dos demais DFe:
        - Não possui o campo tpEmis (forma de emissão)
        - O campo serie tem 9 dígitos (em vez de 3)
        - O campo nNF tem 6 dígitos (em vez de 9)
        - O campo cNF tem 6 dígitos (em vez de 8)

    Estrutura:
        cUF(2) dhEmi(4) CNPJ(14) mod(2) serie(9) nNF(6) cNF(6) cDV(1)
    """

    CHAVE_REGEX = re.compile(r"^CFe(?P<campos>\d{44})$")

    SERIE = slice(22, 31)   # 9 dígitos
    NUMERO = slice(31, 37)  # 6 dígitos
    FORMA = slice(0, 0)     # Não existe no CF-e SAT
    CODIGO = slice(37, 43)  # cNF — 6 dígitos
    DV = slice(43, None)


# ---------------------------------------------------------------------------
# Subclasse NFS-e
# ---------------------------------------------------------------------------

class ChaveNFSe:
    """Chave de acesso da NFS-e — Nota Fiscal de Serviço Eletrônica.

    A NFS-e possui estrutura de chave **diferente** dos demais DFe:
    50 dígitos numéricos, sem o campo ``mod`` e com campos específicos como
    ``cMun`` (código do município, 7 dígitos) e ``ambGer`` (ambiente gerador).

    Estrutura da chave (50 dígitos):

         0       7 8 9 10            23              36    40   49 50
         |       | | |  |             |               |     |    |  |
         cMun(7) A T    CNPJ/CPF(14) nNFSe(13)       AAMM  cNF  cDV

    Campos:
        cMun   (slice 0:7)  — Código IBGE do município do emitente (7 dígitos)
        ambGer (slice 7:8)  — Ambiente gerador: 1=Município próprio, 2=Sefin Nacional
        tpInsc (slice 8:9)  — Tipo de inscrição: 1=CPF, 2=CNPJ
        CNPJ   (slice 9:23) — CNPJ ou CPF do emitente (14 posições)
        nNFSe  (slice 23:36)— Número da NFS-e (13 dígitos)
        AAMM   (slice 36:40)— Ano e Mês de emissão
        cNF    (slice 40:49)— Código numérico aleatório (9 dígitos)
        cDV    (slice 49:50)— Dígito verificador (módulo 11)
    """

    # Slices dos campos da chave NFS-e (50 dígitos)
    CMUN = slice(0, 7)
    AMBGER = slice(7, 8)
    TPINSC = slice(8, 9)
    CNPJ_CPF = slice(9, 23)
    NNFSE = slice(23, 36)
    AAMM = slice(36, 40)
    CNF = slice(40, 49)
    DV = slice(49, None)

    # Ambientes geradores válidos
    AMBGER_MUNICIPIO = "1"
    AMBGER_SEFIN = "2"

    def __init__(
        self,
        chave=False,
        # Nomes dos campos da NFS-e
        cMun=False,
        ambGer=False,
        tpInsc=False,
        CNPJ=False,
        CPF=False,
        nNFSe=False,
        dhEmi=False,
        cNF=False,
        validar=False,
    ):
        """Inicializa a chave NFS-e a partir de uma chave completa ou dos campos.

        Args:
            chave (str, optional): Chave de acesso completa com 50 dígitos.
            cMun (str|int, optional): Código IBGE do município do emitente (7 dígitos).
            ambGer (str|int, optional): Ambiente gerador (1=Município, 2=Sefin Nacional).
            tpInsc (str|int, optional): Tipo de inscrição federal (1=CPF, 2=CNPJ).
            CNPJ (str, optional): CNPJ do emitente (com ou sem pontuação).
            CPF (str, optional): CPF do emitente (com ou sem pontuação).
            nNFSe (str|int, optional): Número da NFS-e (até 13 dígitos).
            dhEmi (str, optional): Ano e mês de emissão no formato AAMM (4 dígitos).
            cNF (str, optional): Código numérico aleatório (9 dígitos). Se não
                informado, é gerado deterministicamente.
            validar (bool, optional): Se True, valida a chave após a geração/parse.

        Raises:
            ValueError: Se os campos obrigatórios estiverem ausentes ou a chave
                for inválida.
        """
        if not chave:
            if not (cMun and ambGer and tpInsc and (CNPJ or CPF) and nNFSe and dhEmi):
                raise ValueError("Impossível gerar a chave NFS-e: campos obrigatórios ausentes.")

            _doc = punctuation_rm(CNPJ or CPF)
            campos = str(cMun).zfill(self.CMUN.stop - self.CMUN.start)
            campos += str(ambGer).zfill(self.AMBGER.stop - self.AMBGER.start)
            campos += str(tpInsc).zfill(self.TPINSC.stop - self.TPINSC.start)
            campos += str(_doc).zfill(self.CNPJ_CPF.stop - self.CNPJ_CPF.start)
            campos += str(nNFSe).zfill(self.NNFSE.stop - self.NNFSE.start)
            campos += str(dhEmi)

            if not cNF:
                cNF = self._calculo_codigo_aleatorio(campos)
            campos += str(cNF).zfill(self.CNF.stop - self.CNF.start)
            campos += str(modulo11(campos))
        else:
            matcher = CHAVE_NFSE_REGEX.match(chave)
            if not matcher:
                raise ValueError("Chave NFS-e inválida (esperado 50 dígitos): {!r}".format(chave))
            campos = matcher.group("campos")

        self._campos = campos
        self._chave = campos

        if validar:
            self.validar()

    # -----------------------------------------------------------------------
    # Geração do código numérico
    # -----------------------------------------------------------------------

    def _calculo_codigo_aleatorio(self, campos):
        """Calcula o cNF deterministicamente a partir dos campos já montados.

        Args:
            campos (str): String parcial da chave (sem cNF e cDV).

        Returns:
            str: Código numérico com 9 dígitos.
        """
        tamanho = self.CNF.stop - self.CNF.start
        soma = sum(int(c) ** 3 ** 2 for c in campos)
        codigo = str(soma)
        if len(codigo) > tamanho:
            return codigo[-tamanho:]
        return codigo.rjust(tamanho, "0")

    # -----------------------------------------------------------------------
    # Validação
    # -----------------------------------------------------------------------

    def validar(self):
        """Valida a chave de acesso da NFS-e.

        Validações realizadas:
            - Tamanho: exatamente 50 dígitos numéricos
            - ambGer: valor 1 ou 2
            - tpInsc: valor 1 (CPF) ou 2 (CNPJ)
            - CNPJ/CPF do emitente: dígitos verificadores válidos
            - cDV: dígito verificador da chave (módulo 11 sobre os 49 primeiros dígitos)

        Raises:
            ValueError: Se qualquer validação falhar, com mensagem descritiva.
        """
        if len(self._campos) != 50 or not self._campos.isdigit():
            raise ValueError(
                "Chave NFS-e inválida (deve ter 50 dígitos numéricos): {!r}".format(self._chave)
            )

        # Verifica ambGer
        if self._campos[self.AMBGER] not in (self.AMBGER_MUNICIPIO, self.AMBGER_SEFIN):
            raise ValueError(
                "Chave NFS-e inválida (ambGer {!r} não permitido): {!r}".format(
                    self._campos[self.AMBGER], self._chave
                )
            )

        # Verifica tpInsc
        if self._campos[self.TPINSC] not in TP_INSC_NFSE:
            raise ValueError(
                "Chave NFS-e inválida (tpInsc {!r} desconhecido, esperado 1=CPF ou 2=CNPJ): {!r}".format(
                    self._campos[self.TPINSC], self._chave
                )
            )

        # Verifica CNPJ ou CPF do emitente
        tp = self._campos[self.TPINSC]
        doc_raw = self._campos[self.CNPJ_CPF]
        if tp == "1":  # CPF — ocupa os 11 últimos dígitos das 14 posições
            doc_para_validar = doc_raw[3:]
        else:          # CNPJ
            doc_para_validar = doc_raw
        if not cnpj_cpf.validar(doc_para_validar):
            raise ValueError(
                "Chave NFS-e inválida ({} emitente inválido: {!r}): {!r}".format(
                    TP_INSC_NFSE[tp],
                    cnpj_cpf.formata(doc_para_validar),
                    self._chave,
                )
            )

        # Verifica cDV (módulo 11 sobre os 49 primeiros dígitos)
        digito = modulo11(self._campos[:49])
        if digito != int(self._campos[49]):
            raise ValueError(
                "Dígito verificador inválido na chave NFS-e: "
                "chave={!r}, dígito calculado={!r}".format(self._chave, digito)
            )

    # -----------------------------------------------------------------------
    # Representação
    # -----------------------------------------------------------------------

    def __str__(self):
        return self._chave

    def __repr__(self):
        return "ChaveNFSe({!r})".format(self._chave)

    # -----------------------------------------------------------------------
    # Propriedades
    # -----------------------------------------------------------------------

    @property
    def chave(self):
        """Chave de acesso completa (50 dígitos)."""
        return self._chave

    @property
    def dfe_key(self):
        """Alias para a chave de acesso completa."""
        return self._chave

    @property
    def campos(self):
        """String interna com os 50 dígitos da chave."""
        return self._campos

    @property
    def cMun(self):
        """Código IBGE do município do emitente (str, 3 dígitos)."""
        return self._campos[self.CMUN]

    @property
    def ambGer(self):
        """Ambiente gerador da NFS-e (str, 1 dígito).

        Returns:
            str: '1' para sistema próprio do município, '2' para Sefin Nacional.
        """
        return self._campos[self.AMBGER]

    @property
    def ambGer_descricao(self):
        """Descrição textual do ambiente gerador."""
        return {
            self.AMBGER_MUNICIPIO: "Sistema Próprio do Município",
            self.AMBGER_SEFIN: "Sefin Nacional NFS-e",
        }.get(self.ambGer, "Ambiente desconhecido: {!r}".format(self.ambGer))

    @property
    def tpInsc(self):
        """Tipo de inscrição federal do emitente (str, 1 dígito).

        Returns:
            str: '1' para CPF, '2' para CNPJ.
        """
        return self._campos[self.TPINSC]

    @property
    def tpInsc_descricao(self):
        """Descrição textual do tipo de inscrição federal."""
        return TP_INSC_NFSE.get(self.tpInsc, "Tipo desconhecido: {!r}".format(self.tpInsc))

    @property
    def cnpj_cpf_emitente(self):
        """CNPJ ou CPF do emitente formatado."""
        doc_raw = self._campos[self.CNPJ_CPF]
        if self.tpInsc == "1":  # CPF
            return cnpj_cpf.formata(doc_raw[3:])
        return cnpj_cpf.formata(doc_raw)

    @property
    def nNFSe(self):
        """Número da NFS-e (str, 13 dígitos)."""
        return self._campos[self.NNFSE]

    @property
    def dhEmi(self):
        """Ano e Mês de emissão no formato AAMM (str, 4 dígitos)."""
        return self._campos[self.AAMM]

    @property
    def ano_emissao(self):
        """Ano de emissão (int, ex: 2024)."""
        return int(self._campos[self.AAMM][:2]) + 2000

    @property
    def mes_emissao(self):
        """Mês de emissão (int, 1-12)."""
        return int(self._campos[self.AAMM][2:])

    @property
    def cNF(self):
        """Código numérico aleatório que compõe a chave (str, 9 dígitos)."""
        return self._campos[self.CNF]

    @property
    def cDV(self):
        """Dígito verificador da chave de acesso (str, 1 dígito)."""
        return self._campos[self.DV]
