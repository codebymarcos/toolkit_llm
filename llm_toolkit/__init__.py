"""LLM Toolkit - Chat local com Gemma 2B"""

from .core.llm import gerar_resposta
from .api import GeradorLLM, obter_gerador, ClienteAPI
from .client.models import RespostaCliente
from .config import config
from .constantes import *

__all__ = [
    "gerar_resposta",
    "GeradorLLM",
    "obter_gerador",
    "ClienteAPI",
    "RespostaCliente",
    "config"
]
__version__ = "1.0.0"


