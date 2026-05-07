# Copyright (C) 2015  Base4 Sistemas Ltda ME
# Copyright (C) 2020  Luis Felipe Mileo - KMEE
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

"""Módulo de retrocompatibilidade — o código foi movido para ``dfe.py``.

.. deprecated::
    Importe diretamente de ``erpbrasil.base.fiscal.dfe``:

    - ``ChaveEdoc``      → :class:`~erpbrasil.base.fiscal.dfe.ChaveDFe`
    - ``detectar_chave_edoc`` → :func:`~erpbrasil.base.fiscal.dfe.detectar_chave_dfe`

    Os aliases abaixo são mantidos para garantir compatibilidade com código
    existente e serão removidos em uma versão futura.
"""

from .dfe import CHAVE_REGEX
from .dfe import CODIGO_ESTADOS_IBGE
from .dfe import CODIGO_MODELOS_EDOC
from .dfe import EDOC_PREFIX
from .dfe import ESTADOS_IBGE
from .dfe import MODELOS_SITE_AUTORIZ
from .dfe import ChaveCFeSAT
from .dfe import ChaveDFe as ChaveEdoc
from .dfe import detectar_chave_dfe as detectar_chave_edoc

__all__ = [
    # Aliases legados
    "ChaveEdoc",
    "ChaveCFeSAT",
    "detectar_chave_edoc",
    # Constantes
    "ESTADOS_IBGE",
    "CODIGO_ESTADOS_IBGE",
    "EDOC_PREFIX",
    "CODIGO_MODELOS_EDOC",
    "CHAVE_REGEX",
    "MODELOS_SITE_AUTORIZ",
]
