# See http://peak.telecommunity.com/DevCenter/setuptools#namespace-packages
from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
