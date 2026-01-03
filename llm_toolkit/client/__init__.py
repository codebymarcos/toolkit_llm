"""Cliente Python para interagir com a API REST"""

from .models import RespostaCliente
from .api import ClienteAPI

__all__ = ["ClienteAPI", "RespostaCliente"]

