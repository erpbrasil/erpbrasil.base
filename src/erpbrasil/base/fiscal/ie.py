# coding=utf-8
# Copyright (C) 2013  Renato Lima - Akretion
# Copyright (C) 2023  Gabriel Krauss - KMEE
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import re

PARAMETERS = {
    "ac": {
        "tam": 13,
        "val_tam": 11,
        "starts_with": "01",
        "format": lambda x: "{0}.{1}.{2}/{3}-{4}".format(
            x[:2], x[2:5], x[5:8], x[8:11], x[11:13]
        ),
    },
    "al": {
        "tam": 9,
        "starts_with": "24",
        "format": lambda x: "{0}.{1}.{2}-{3}".format(x[:2], x[2:5], x[5:8], x[8:9]),
    },
    "am": {
        "tam": 9,
        "format": lambda x: "{0}.{1}.{2}-{3}".format(x[:2], x[2:5], x[5:8], x[8:9]),
    },
    "ce": {"tam": 9, "format": lambda x: "{0}.{1}-{2}".format(x[:2], x[2:8], x[8:9])},
    "df": {
        "tam": 13,
        "val_tam": 11,
        "starts_with": "07",
        "format": lambda x: "{0}-{1}.{2}/{3}-{4}".format(
            x[:2], x[2:5], x[5:8], x[8:11], x[11:13]
        ),
    },
    "es": {
        "tam": 9,
        "format": lambda x: "{0}.{1}.{2}-{3}".format(x[:3], x[3:6], x[6:8], x[8:9]),
    },
    "ma": {
        "tam": 9,
        "starts_with": "12",
        "format": lambda x: "{0}.{1}.{2}-{3}".format(x[:2], x[2:5], x[5:8], x[8:9]),
    },
    "mt": {
        "tam": 11,
        "prod": [3, 2, 9, 8, 7, 6, 5, 4, 3, 2],
        "format": lambda x: "{0}.{1}.{2}.{3}-{4}".format(
            x[:2], x[2:4], x[4:6], x[6:10], x[10:11]
        ),
    },
    "ms": {
        "tam": 9,
        "starts_with": "28",
        "format": lambda x: "{0}.{1}.{2}-{3}".format(x[:2], x[2:5], x[5:8], x[8:9]),
    },
    "pa": {
        "tam": 9,
        "starts_with": "15",
        "format": lambda x: "{0}.{1}.{2}-{3}".format(x[:2], x[2:5], x[5:8], x[8:9]),
    },
    "pb": {
        "tam": 9,
        "format": lambda x: "{0}.{1}.{2}-{3}".format(x[:2], x[2:5], x[5:8], x[8:9]),
    },
    "pr": {
        "tam": 10,
        "val_tam": 8,
        "prod": [3, 2, 7, 6, 5, 4, 3, 2],
        "format": lambda x: "{0}.{1}-{2}".format(x[:3], x[3:7], x[7:9]),
    },
    "pi": {
        "tam": 9,
        "format": lambda x: "{0}.{1}.{2}-{3}".format(x[:2], x[2:5], x[5:8], x[8:9]),
    },
    "rj": {
        "tam": 8,
        "prod": [2, 7, 6, 5, 4, 3, 2],
        "format": lambda x: "{0}.{1}.{2}-{3}".format(x[:2], x[2:5], x[5:7], x[7:8]),
    },
    "rn": {"tam": 10, "val_tam": 9, "prod": [10, 9, 8, 7, 6, 5, 4, 3, 2]},
    "rs": {
        "tam": 10,
        "format": lambda x: "{0}/{1}.{2}-{3}".format(x[:3], x[3:6], x[6:9], x[9:10]),
    },
    "rr": {
        "tam": 9,
        "starts_with": "24",
        "prod": [1, 2, 3, 4, 5, 6, 7, 8],
        "div": 9,
        "format": lambda x: "{0}.{1}.{2}-{3}".format(x[:2], x[2:5], x[5:8], x[8:9]),
    },
    "sc": {"tam": 9, "format": lambda x: "{0}.{1}.{2}".format(x[:3], x[3:6], x[6:9])},
    "se": {
        "tam": 9,
        "format": lambda x: "{0}.{1}.{2}-{3}".format(x[:2], x[2:5], x[5:8], x[8:9]),
    },
    "to": {
        "tam": 9,
        "prod": [9, 8, 7, 6, 5, 4, 3, 2],
        "format": lambda x: "{0}.{1}.{2}-{3}".format(x[:2], x[2:5], x[5:8], x[8:9]),
    },
}


def validar(uf, inscr_est):
    result = True
    try:
        validar_by_uf = globals()["validar_%s" % uf]
        if not validar_by_uf(inscr_est):
            result = False
    except KeyError:
        if not validar_param(uf, inscr_est):
            result = False
    return result


def validar_param(uf, inscr_est):
    if uf not in PARAMETERS:
        return True

    tam = PARAMETERS[uf].get("tam", 0)
    inscr_est = inscr_est.strip().rjust(int(tam), "0")
    inscr_est = re.sub("[^0-9]", "", inscr_est)
    val_tam = PARAMETERS[uf].get("val_tam", tam - 1)

    if isinstance(tam, list):
        i = tam.find(len(inscr_est))
        if i == -1:
            return False
        else:
            val_tam = val_tam[i]
    else:
        if len(inscr_est) != tam:
            return False

    sw = PARAMETERS[uf].get("starts_with", "")
    if not inscr_est.startswith(sw):
        return False

    inscr_est_ints = [int(c) for c in inscr_est]
    nova_ie = inscr_est_ints[:val_tam]
    prod = PARAMETERS[uf].get("prod", [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    prod = prod[-val_tam:]

    while len(nova_ie) < tam:
        r = sum([x * y for (x, y) in zip(nova_ie, prod)]) % PARAMETERS[uf].get(
            "div", 11
        )

        if r > 1:
            f = 11 - r
        else:
            f = 0

        if uf not in "rr":
            nova_ie.append(f)
        else:
            nova_ie.append(r)
        prod.insert(0, prod[0] + 1)

    # Se o número gerado coincidir com o número original, é válido
    return nova_ie == inscr_est_ints


def validar_ap(inscr_est):
    inscr_est = re.sub("[^0-9]", "", inscr_est)

    # verificando o tamanho da inscrição estadual
    if len(inscr_est) != 9:
        return False

    # verificando os dois primeiros dígitos
    if not inscr_est.startswith("03"):
        return False

    # Pega apenas os 8 primeiros dígitos da inscrição estadual e
    # define os valores de 'p' e 'd'
    inscr_est_int = int(inscr_est[:8])
    if inscr_est_int <= 3017000:
        inscr_est_p = 5
        inscr_est_d = 0
    elif inscr_est_int <= 3019022:
        inscr_est_p = 9
        inscr_est_d = 1
    else:
        inscr_est_p = 0
        inscr_est_d = 0

    # Pega apenas os 8 primeiros dígitos da inscrição estadual e
    # gera o dígito verificador
    inscr_est = list(map(int, inscr_est))
    nova_ie = inscr_est[:8]

    prod = [9, 8, 7, 6, 5, 4, 3, 2]
    r = (inscr_est_p + sum([x * y for (x, y) in zip(nova_ie, prod)])) % 11
    if r > 1:
        f = 11 - r
    elif r == 1:
        f = 0
    else:
        f = inscr_est_d
    nova_ie.append(f)

    return nova_ie == inscr_est


def validar_ba(inscr_est):
    inscr_est = re.sub("[^0-9]", "", inscr_est)
    inscr_est = list(map(int, inscr_est))

    # verificando o tamanho da inscrição estadual
    if len(inscr_est) == 8:
        tam = 8
        val_tam = 6
        test_digit = 0
    elif len(inscr_est) == 9:
        tam = 9
        val_tam = 7
        test_digit = 1
    else:
        return False

    nova_ie = inscr_est[:val_tam]

    prod = [8, 7, 6, 5, 4, 3, 2][-val_tam:]

    if inscr_est[test_digit] in [0, 1, 2, 3, 4, 5, 8]:
        modulo = 10
    else:
        modulo = 11

    while len(nova_ie) < tam:
        r = sum([x * y for (x, y) in zip(nova_ie, prod)]) % modulo
        if r > 0:
            f = modulo - r
        else:
            f = 0

        if f >= 10 and modulo == 11:
            f = 0

        if len(nova_ie) == val_tam:
            nova_ie.append(f)
        else:
            nova_ie.insert(val_tam, f)
        prod.insert(0, prod[0] + 1)

    return nova_ie == inscr_est


def validar_go(inscr_est):
    inscr_est = re.sub("[^0-9]", "", inscr_est)

    # verificando o tamanho da inscrição estadual
    if len(inscr_est) != 9:
        return False

    # verificando os dois primeiros dígitos
    # https://agenciacoradenoticias.go.gov.br/63140-empreendedorismo-governo-de-goias-altera-no-de-inscricao-estadual-para-novos-cadastros
    if inscr_est[:2] not in ["10", "11", "20"]:
        return False

    # Pega apenas os 8 primeiros dígitos da inscrição estadual e
    # define os valores de 'p' e 'd'
    inscr_est_int = int(inscr_est[:8])
    if inscr_est_int >= 10103105 and inscr_est_int <= 10119997:
        inscr_est_d = 1
    else:
        inscr_est_d = 0

    # Pega apenas os 8 primeiros dígitos da inscrição estadual e
    # gera o dígito verificador
    inscr_est = list(map(int, inscr_est))
    nova_ie = inscr_est[:8]

    prod = [9, 8, 7, 6, 5, 4, 3, 2]
    r = sum([x * y for (x, y) in zip(nova_ie, prod)]) % 11
    if r > 1:
        f = 11 - r
    elif r == 1:
        f = inscr_est_d
    else:
        f = 0
    nova_ie.append(f)

    return nova_ie == inscr_est


def validar_mg(inscr_est):
    # A validação de produtor rural foi padronizada com a normal em MG

    # A partir de 02 de março de 2009, todos os produtores rurais, pessoa física, de Minas Gerais,
    # tiveram que se inscrever no cadastro informatizado da Secretaria de Estado de Fazenda
    # (SEF-MG), conforme estabelecido pelo Decreto 45.030, de 29 de fevereiro de 2009.
    # A inscrição antiga foi substituída pela Inscrição Estadual de Produtor Rural
    # com 13 dígitos, padrão para os contribuintes mineiros,
    # devendo ser informada normalmente no arquivo eletrônico.

    # Fonte: http://www.fazenda.mg.gov.br/empresas/ped/duvidas_frequentes/

    inscr_est = re.sub("[^0-9]", "", inscr_est)

    # verificando o tamanho da inscrição estadual
    if len(inscr_est) != 13:
        return False

    # Pega apenas os 11 primeiros dígitos da inscrição estadual e
    # gera os dígitos verificadores
    inscr_est = list(map(int, inscr_est))
    nova_ie = inscr_est[:11]

    nova_ie_aux = list(nova_ie)
    nova_ie_aux.insert(3, 0)
    prod = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
    r = str([x * y for (x, y) in zip(nova_ie_aux, prod)])
    r = re.sub("[^0-9]", "", r)
    r = list(map(int, r))
    r = sum(r)
    r2 = (r // 10 + 1) * 10
    r = r2 - r

    if r >= 10:
        r = 0

    nova_ie.append(r)

    prod = [3, 2, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    r = sum([x * y for (x, y) in zip(nova_ie, prod)]) % 11
    if r > 1:
        f = 11 - r
    else:
        f = 0
    nova_ie.append(f)

    return nova_ie == inscr_est


def validar_pe(inscr_est):
    inscr_est = re.sub("[^0-9]", "", inscr_est)

    # verificando o tamanho da inscrição estadual
    if (len(inscr_est) != 9) and (len(inscr_est) != 14):
        return False

    inscr_est = list(map(int, inscr_est))

    # verificando o tamanho da inscrição estadual
    if len(inscr_est) == 9:
        # Pega apenas os 7 primeiros dígitos da inscrição estadual e
        # gera os dígitos verificadores
        inscr_est = list(map(int, inscr_est))
        nova_ie = inscr_est[:7]

        prod = [8, 7, 6, 5, 4, 3, 2]
        while len(nova_ie) < 9:
            r = sum([x * y for (x, y) in zip(nova_ie, prod)]) % 11
            if r > 1:
                f = 11 - r
            else:
                f = 0
            nova_ie.append(f)
            prod.insert(0, 9)
    elif len(inscr_est) == 14:
        # Pega apenas os 13 primeiros dígitos da inscrição estadual e
        # gera o dígito verificador
        inscr_est = list(map(int, inscr_est))
        nova_ie = inscr_est[:13]

        prod = [5, 4, 3, 2, 1, 9, 8, 7, 6, 5, 4, 3, 2]
        r = sum([x * y for (x, y) in zip(nova_ie, prod)]) % 11
        f = 11 - r
        if f > 10:
            f = f - 10
        nova_ie.append(f)

    return nova_ie == inscr_est


def validar_rn(inscr_est):
    def gera_digito_rn(nova_ie, prod):
        r = (sum([x * y for (x, y) in zip(nova_ie, prod)]) * 10) % 11
        if r == 10:
            r = 0
        return r

    inscr_est = re.sub("[^0-9]", "", inscr_est)
    inscr_est = list(map(int, inscr_est))
    aux = [2, 0]
    if inscr_est[:2] == aux[:2]:
        if len(inscr_est) == 9:
            nova_ie = inscr_est[:8]
            prod = [9, 8, 7, 6, 5, 4, 3, 2]
            f = gera_digito_rn(nova_ie, prod)
            nova_ie.append(f)

        elif len(inscr_est) == 10:
            nova_ie = inscr_est[:9]
            prod = [10, 9, 8, 7, 6, 5, 4, 3, 2]
            f = gera_digito_rn(nova_ie, prod)
            nova_ie.append(f)
        else:
            return False
    else:
        return False

    return nova_ie == inscr_est


def validar_ro(inscr_est):
    def gera_digito_ro(nova_ie, prod):
        r = sum([x * y for (x, y) in zip(nova_ie, prod)]) % 11
        f = 11 - r
        if f > 9:
            f = f - 10
        return f

    inscr_est = re.sub("[^0-9]", "", inscr_est)
    inscr_est = list(map(int, inscr_est))

    # verificando o tamanho da inscrição estadual
    if len(inscr_est) == 9:
        # Despreza-se os 3 primeiros dígitos, pega apenas os 8 primeiros
        # dígitos da inscrição estadual e gera o dígito verificador
        nova_ie = inscr_est[3:8]

        prod = [6, 5, 4, 3, 2]
        f = gera_digito_ro(nova_ie, prod)
        nova_ie.append(f)

        nova_ie = inscr_est[0:3] + nova_ie
    elif len(inscr_est) == 14:
        # Pega apenas os 13 primeiros dígitos da inscrição estadual e
        # gera o dígito verificador
        nova_ie = inscr_est[:13]

        prod = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        f = gera_digito_ro(nova_ie, prod)
        nova_ie.append(f)
    else:
        return False

    return nova_ie == inscr_est


def validar_sp(inscr_est):
    def gera_digito_sp(nova_ie, prod):
        r = sum([x * y for (x, y) in zip(nova_ie, prod)]) % 11
        if r < 10:
            return r
        elif r == 10:
            return 0
        else:
            return 1

    def gera_digito_sp_pr(nova_ie, prod):
        r = sum([x * y for (x, y) in zip(nova_ie, prod)]) % 11
        return r

    # Industriais e comerciais
    if inscr_est[0] != "P":
        inscr_est = re.sub("[^0-9]", "", inscr_est)

        # verificando o tamanho da inscrição estadual
        if len(inscr_est) != 12:
            return False

        # Pega apenas os 8 primeiros dígitos da inscrição estadual e
        # gera o primeiro dígito verificador
        inscr_est = list(map(int, inscr_est))
        nova_ie = inscr_est[:8]

        prod = [1, 3, 4, 5, 6, 7, 8, 10]
        f = gera_digito_sp(nova_ie, prod)
        nova_ie.append(f)

        # gera o segundo dígito verificador
        nova_ie.extend(inscr_est[9:11])
        prod = [3, 2, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        f = gera_digito_sp(nova_ie, prod)
        nova_ie.append(f)

    # Produtor rural
    else:
        inscr_est = re.sub("[^0-9]", "", inscr_est)

        # verificando o tamanho da inscrição estadual
        if len(inscr_est) != 12:
            return False

        # verificando o primeiro dígito depois do 'P'
        if inscr_est[0] != "0":
            return False

        # Pega apenas os 8 primeiros dígitos da inscrição estadual e
        # gera o dígito verificador
        inscr_est = list(map(int, inscr_est))
        nova_ie = inscr_est[:8]

        prod = [1, 3, 4, 5, 6, 7, 8, 10]
        f = gera_digito_sp_pr(nova_ie, prod)
        nova_ie.append(f)

        nova_ie.extend(inscr_est[9:])

    return nova_ie == inscr_est


def validar_to(inscr_est):
    """
    Calculo a partir de junho de 2002
    http://www2.sefaz.to.gov.br/Servicos/Sintegra/calinse.htm
    http://dtri.sefaz.to.gov.br/legislacao/ntributaria/portarias/sefaz/Portaria676-02.htm

    """
    inscr_est = re.sub("[^0-9]", "", inscr_est)

    # verificando o tamanho da inscrição estadual
    if len(inscr_est) != 9:
        return False

    # Pega apenas os dígitos que entram no cálculo
    inscr_est = list(map(int, inscr_est))
    nova_ie = inscr_est[:8]

    prod = [9, 8, 7, 6, 5, 4, 3, 2]
    r = sum([x * y for (x, y) in zip(nova_ie, prod)]) % 11
    if r > 1:
        f = 11 - r
    else:
        f = 0
    nova_ie.append(f)
    return nova_ie == inscr_est


def formata(uf, inscr_est):
    try:
        formata_by_uf = globals()["formata_%s" % uf]
        inscr_est = formata_by_uf(inscr_est)
    except KeyError:
        inscr_est = re.sub("[^0-9]", "", inscr_est)
        inscr_est = formata_param(uf, inscr_est)

    return inscr_est


def formata_param(uf, inscr_est):
    if uf not in PARAMETERS:
        return inscr_est

    tam = PARAMETERS[uf].get("tam", 0)
    inscr_est = inscr_est.strip().rjust(int(tam), "0")
    inscr_est = re.sub("[^0-9]", "", inscr_est)

    if len(inscr_est) == tam:
        format_lambda = PARAMETERS[uf].get("format")
        inscr_est = format_lambda(inscr_est)

    return inscr_est


def formata_ap(inscr_est):
    tam = 9
    inscr_est = inscr_est.strip().rjust(int(tam), "0")
    inscr_est = re.sub("[^0-9]", "", inscr_est)
    if len(inscr_est) == tam:
        inscr_est = "{0}.{1}.{2}-{3}".format(
            inscr_est[:2], inscr_est[2:5], inscr_est[5:8], inscr_est[8:9]
        )
    return inscr_est


def formata_ba(inscr_est):
    inscr_est = re.sub("[^0-9]", "", inscr_est)
    if len(inscr_est) == 8:
        inscr_est = inscr_est.rjust(9, "0")
    if len(inscr_est) == 9:
        inscr_est = "{0}.{1}.{2}".format(inscr_est[:3], inscr_est[3:6], inscr_est[6:9])

    return inscr_est


def formata_go(inscr_est):
    tam = 9
    inscr_est = inscr_est.strip().rjust(int(tam), "0")
    inscr_est = re.sub("[^0-9]", "", inscr_est)
    if len(inscr_est) == tam:
        inscr_est = "{0}.{1}.{2}-{3}".format(
            inscr_est[:2], inscr_est[2:5], inscr_est[5:8], inscr_est[8:9]
        )

    return inscr_est


def formata_mg(inscr_est):
    inscr_est = re.sub("[^0-9]", "", inscr_est)
    if len(inscr_est) == 13:
        inscr_est = "{0}.{1}.{2}/{3}-{4}".format(
            inscr_est[:3],
            inscr_est[3:6],
            inscr_est[6:9],
            inscr_est[9:11],
            inscr_est[11:13],
        )
    return inscr_est


def formata_pe(inscr_est):
    inscr_est = re.sub("[^0-9]", "", inscr_est)
    if len(inscr_est) == 9:
        inscr_est = "{0}-{1}".format(inscr_est[:7], inscr_est[7:9])

    if len(inscr_est) == 14:
        inscr_est = "{0}.{1}.{2}.{3}-{4}".format(
            inscr_est[:2], inscr_est[2], inscr_est[3:6], inscr_est[6:13], inscr_est[13]
        )
    return inscr_est


def formata_rn(inscr_est):
    inscr_est = re.sub("[^0-9]", "", inscr_est)
    if len(inscr_est) == 9:
        inscr_est = "{0}.{1}.{2}-{3}".format(
            inscr_est[:2], inscr_est[2:5], inscr_est[5:8], inscr_est[8:9]
        )

    if len(inscr_est) == 10:
        inscr_est = "{0}.{1}.{2}-{3}".format(
            inscr_est[:3], inscr_est[3:6], inscr_est[6:9], inscr_est[9:10]
        )
    return inscr_est


def formata_sp(inscr_est):
    # Adicionar a formatação para IEs normal e para produtor rural
    if re.match("P", inscr_est) is None:
        # Se IE normal
        inscr_est = re.sub("[^0-9]", "", inscr_est)
        if len(inscr_est) == 12:
            inscr_est = "{0}.{1}.{2}.{3}".format(
                inscr_est[:3], inscr_est[3:6], inscr_est[6:9], inscr_est[9:12]
            )
    else:
        # Se produtor rural
        inscr_est = re.sub("[^0-9]", "", inscr_est)
        if len(inscr_est) == 12:
            inscr_est = "P-{0}.{1}/{2}".format(
                inscr_est[:8], inscr_est[8:9], inscr_est[9:12]
            )
    return inscr_est
