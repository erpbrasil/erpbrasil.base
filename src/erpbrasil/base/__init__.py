try:
    from importlib.metadata import PackageNotFoundError, version as _version
except ImportError:  # Python 3.7
    from importlib_metadata import PackageNotFoundError, version as _version


def _versao():
    # hatch-vcs: a versao vem da tag do git; nao ha mais numero fixo aqui.
    # Antes do Python 3.10 o importlib.metadata nao normaliza o nome do pacote
    # (erpbrasil.base x erpbrasil_base), por isso as duas tentativas.
    for nome in ("erpbrasil.base", "erpbrasil_base"):
        try:
            return _version(nome)
        except PackageNotFoundError:
            continue
    return "0.0.0"


__version__ = _versao()

from erpbrasil.base.fiscal import *  # noqa: F403
from erpbrasil.base.misc import *  # noqa: F403
