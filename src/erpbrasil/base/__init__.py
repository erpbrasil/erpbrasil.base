try:
    from importlib.metadata import version as _version
except ImportError:  # Python 3.7
    from importlib_metadata import version as _version

# hatch-vcs: a versao vem da tag do git; nao ha mais numero fixo aqui
__version__ = _version("erpbrasil.base")

from erpbrasil.base.fiscal import *  # noqa: F403
from erpbrasil.base.misc import *  # noqa: F403
