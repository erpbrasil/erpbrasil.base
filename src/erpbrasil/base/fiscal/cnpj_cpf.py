# coding=utf-8
# Copyright (C) 2013  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

"""Validação e formatação de CNPJ (numérico e alfanumérico) e CPF.

CNPJ Alfanumérico — NT Conjunta 2025.001 (IN RFB nº 2229/2024)
---------------------------------------------------------------
A partir de julho de 2026 o CNPJ passa a aceitar letras maiúsculas nas
primeiras 12 posições (raiz de 8 + ordem de 4). Os dois últimos dígitos
continuam sendo verificadores numéricos.

Algoritmo de DV (módulo 11 com valores ASCII):
    Cada caractere é convertido pelo valor  ``ord(c) - 48``, o que mantém
    os dígitos numéricos com seus valores habituais (0–9) e mapeia letras
    como  A=17, B=18, C=19 …

Letras proibidas (solicitação ENCAT à RFB, pendente confirmação):
    I, O, U, Q, F
"""

import re

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

# Letras proibidas no CNPJ Alfa (conforme solicitação ENCAT/RFB — NT 2025.001)
_LETRAS_PROIBIDAS = frozenset("IOUQF")

# Regex: primeiras 12 posições alfanuméricas + 2 dígitos verificadores
_RE_CNPJ_ALFA = re.compile(r"^[A-Z0-9]{12}[0-9]{2}$")

# Regex para remover máscara (pontos, barra, hífen)
_RE_MASCARA = re.compile(r"[./-]")

# Pesos para cálculo do DV do CNPJ (posições 1-13)
# DV1 usa pesosDV[1:13], DV2 usa pesosDV[0:13]
_PESOS_DV = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]


# ---------------------------------------------------------------------------
# Funções internas
# ---------------------------------------------------------------------------

def _char_value(c):
    """Retorna o valor numérico de um caractere para cálculo de DV.

    Equivalente a ``ord(c) - 48``:
        - Dígitos '0'-'9' → 0-9  (sem alteração em relação ao cálculo antigo)
        - Letras 'A'-'Z'  → 17-42

    Args:
        c (str): Um único caractere (dígito ou letra maiúscula).

    Returns:
        int: Valor numérico do caractere.
    """
    return ord(c) - 48


def _calcular_dv_cnpj(cnpj12):
    """Calcula os dois dígitos verificadores de um CNPJ (sem os DVs).

    Suporta CNPJ puramente numérico e CNPJ alfanumérico.  O algoritmo é
    idêntico — a diferença está no valor atribuído a cada caractere
    (``ord(c) - 48`` em vez de ``int(c)`` direto).

    Args:
        cnpj12 (str): 12 primeiros caracteres do CNPJ (sem DVs),
            em maiúsculas e sem pontuação.

    Returns:
        str: Os dois dígitos verificadores calculados (sempre numéricos).

    Raises:
        ValueError: Se ``cnpj12`` não tiver exatamente 12 posições ou
            contiver caracteres não permitidos.
    """
    if len(cnpj12) != 12:
        raise ValueError(
            "cnpj12 deve ter 12 caracteres, recebido: {!r}".format(cnpj12)
        )

    soma_dv1 = sum(
        _char_value(c) * _PESOS_DV[i + 1]
        for i, c in enumerate(cnpj12)
    )
    dv1 = 0 if soma_dv1 % 11 < 2 else 11 - (soma_dv1 % 11)

    soma_dv2 = sum(
        _char_value(c) * _PESOS_DV[i]
        for i, c in enumerate(cnpj12)
    )
    soma_dv2 += dv1 * _PESOS_DV[12]
    dv2 = 0 if soma_dv2 % 11 < 2 else 11 - (soma_dv2 % 11)

    return "{:d}{:d}".format(dv1, dv2)


def _normalizar_cnpj(cnpj):
    """Remove máscara e converte para maiúsculas.

    Para CNPJs puramente numéricos remove qualquer caractere não-dígito.
    Para CNPJs alfanuméricos remove apenas '.', '/' e '-'.

    Args:
        cnpj (str): CNPJ com ou sem máscara.

    Returns:
        str: CNPJ sem máscara, em maiúsculas.
    """
    cnpj = cnpj.strip().upper()
    cnpj = _RE_MASCARA.sub("", cnpj)
    return cnpj


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

def validar_cnpj(cnpj):
    """Valida um CNPJ numérico ou alfanumérico.

    Suporta:
    - CNPJ numérico clássico (14 dígitos).
    - CNPJ alfanumérico (NT 2025.001): primeiras 12 posições alfanuméricas
      + 2 dígitos verificadores.

    A validação inclui:
    - Tamanho: exatamente 14 caracteres após remoção de máscara.
    - Formato: ``[A-Z0-9]{12}[0-9]{2}``
    - Letras proibidas: ``I, O, U, Q, F`` não são permitidas (NT 2025.001).
    - CNPJ zerado (``00000000000000``) é inválido.
    - Dígitos verificadores calculados pelo módulo 11 com valores ASCII-48.

    Args:
        cnpj (str): CNPJ a ser validado (com ou sem pontuação).

    Returns:
        bool: ``True`` se válido, ``False`` caso contrário.
    """
    if not cnpj:
        return False

    cnpj = _normalizar_cnpj(cnpj)

    if len(cnpj) != 14:
        return False

    # Rejeita CNPJ zerado
    if cnpj == "00000000000000":
        return False

    # Valida formato: 12 alfanuméricos + 2 dígitos
    if not _RE_CNPJ_ALFA.match(cnpj):
        return False

    # Verifica letras proibidas nas 12 primeiras posições
    if _LETRAS_PROIBIDAS & set(cnpj[:12]):
        return False

    # Verifica dígitos verificadores
    dv_informado = cnpj[12:]
    dv_calculado = _calcular_dv_cnpj(cnpj[:12])
    return dv_informado == dv_calculado


def validar_cpf(cpf):
    """Valida um CPF — Cadastro de Pessoa Física.

    Args:
        cpf (str): CPF a ser validado (com ou sem pontuação).

    Returns:
        bool: ``True`` se válido, ``False`` caso contrário.
    """
    if not cpf:
        return False

    cpf = re.sub(r"[^0-9]", "", cpf)

    if len(cpf) != 11 or cpf == cpf[0] * len(cpf):
        return False

    cpf_ints = list(map(int, cpf))
    novo = cpf_ints[:9]

    while len(novo) < 11:
        r = sum([(len(novo) + 1 - i) * v for i, v in enumerate(novo)]) % 11
        novo.append(0 if r < 2 else 11 - r)

    return novo == cpf_ints


def validar(cnpj_cpf=None):
    """Valida um CNPJ ou CPF com base no número de caracteres.

    Regras de roteamento:
    - 14 caracteres (após remoção de máscara de pontuação): trata como CNPJ.
      Suporta CNPJ numérico e alfanumérico (NT 2025.001).
    - 11 dígitos (após remoção de pontuação numérica): trata como CPF.

    Args:
        cnpj_cpf (str): CNPJ ou CPF para ser validado.

    Returns:
        bool | None: ``True`` se válido, ``False`` se inválido,
            ``None`` se ``cnpj_cpf`` for falsy.
    """
    if not cnpj_cpf:
        return None

    # Tenta como CNPJ (remove apenas máscara, preserva letras)
    candidato = _normalizar_cnpj(cnpj_cpf)
    if len(candidato) == 14:
        return validar_cnpj(candidato)

    # Tenta como CPF (remove tudo que não é dígito)
    apenas_digitos = re.sub(r"[^0-9]", "", cnpj_cpf)
    if len(apenas_digitos) == 11:
        return validar_cpf(apenas_digitos)

    return False


def formata_cnpj(cnpj=None):
    """Formata um CNPJ com pontuação (``XX.XXX.XXX/XXXX-XX``).

    Suporta CNPJ numérico e alfanumérico. Para CNPJ alfanumérico, a máscara
    é aplicada sobre os caracteres originais (letras são preservadas).

    Args:
        cnpj (str): CNPJ com 14 caracteres, com ou sem pontuação.

    Returns:
        str: CNPJ formatado, ou a string original se não tiver 14 caracteres.
    """
    if not cnpj:
        return cnpj

    cnpj = _normalizar_cnpj(cnpj)
    if len(cnpj) == 14:
        return "{}.{}.{}/{}-{}".format(
            cnpj[0:2],
            cnpj[2:5],
            cnpj[5:8],
            cnpj[8:12],
            cnpj[12:14],
        )
    return cnpj


def formata_cpf(cpf=None):
    """Formata um CPF com pontuação (``XXX.XXX.XXX-XX``).

    Args:
        cpf (str): CPF com 11 dígitos, com ou sem pontuação.

    Returns:
        str: CPF formatado, ou a string original se não tiver 11 dígitos.
    """
    if not cpf:
        return cpf

    cpf = re.sub(r"[^0-9]", "", cpf)
    if len(cpf) == 11:
        return "{}.{}.{}-{}".format(cpf[0:3], cpf[3:6], cpf[6:9], cpf[9:11])
    return cpf


def formata(cnpj_cpf=None):
    """Formata um CNPJ ou CPF com pontuação conforme o número de caracteres.

    Args:
        cnpj_cpf (str): CNPJ (14 chars) ou CPF (11 dígitos).

    Returns:
        str | None: String formatada, ou ``None`` se ``cnpj_cpf`` for falsy.
    """
    if not cnpj_cpf:
        return None

    candidato = _normalizar_cnpj(cnpj_cpf)
    if len(candidato) == 14:
        return formata_cnpj(candidato)

    apenas_digitos = re.sub(r"[^0-9]", "", cnpj_cpf)
    if len(apenas_digitos) == 11:
        return formata_cpf(apenas_digitos)

    return cnpj_cpf
