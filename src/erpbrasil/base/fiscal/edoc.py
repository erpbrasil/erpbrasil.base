# Copyright (C) 2015  Base4 Sistemas Ltda ME
# Copyright (C) 2020  Luis Felipe Mileo - KMEE
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

"""Módulo de retrocompatibilidade - o código foi movido para ``dfe.py``.

.. deprecated::
    Importe diretamente de ``erpbrasil.base.fiscal.dfe``:

    - ``ChaveEdoc``      -> :class:`~erpbrasil.base.fiscal.dfe.ChaveDFe`
    - ``detectar_chave_edoc`` -> :func:`~erpbrasil.base.fiscal.dfe.detectar_chave_dfe`

    Os aliases abaixo são mantidos para garantir compatibilidade com código
    existente e serão removidos em uma versão futura.
"""

from .dfe import (
    CHAVE_REGEX,
    CODIGO_ESTADOS_IBGE,
    CODIGO_MODELOS_EDOC,
    EDOC_PREFIX,
    ESTADOS_IBGE,
    MODELOS_SITE_AUTORIZ,
    ChaveCFeSAT,
    ChaveDFe as ChaveEdoc,
    detectar_chave_dfe as detectar_chave_edoc,
)

__all__ = [
    "CHAVE_REGEX",
    "CODIGO_ESTADOS_IBGE",
    "CODIGO_MODELOS_EDOC",
    "EDOC_PREFIX",
    # Constantes
    "ESTADOS_IBGE",
    "MODELOS_SITE_AUTORIZ",
    "ChaveCFeSAT",
    # Aliases legados
    "ChaveEdoc",
    "detectar_chave_edoc",
]
