"""Camada HTTP com decoradores e tratamento centralizado"""

import logging
from functools import wraps
from typing import Dict, Any, Optional, Callable
import requests

logger = logging.getLogger(__name__)


def com_retry(tentativas: int = 3, delay: float = 0.5):
    """Decorador para retry automático"""
    def decorador(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for tentativa in range(tentativas):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if tentativa == tentativas - 1:
                        logger.error(f"{func.__name__} falhou após {tentativas} tentativas: {e}")
                        return None
                    logger.warning(f"{func.__name__} tentativa {tentativa + 1} falhou, retentando...")
            return None
        return wrapper
    return decorador


def com_logging(func: Callable) -> Callable:
    """Decorador para logging automático"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Executando {func.__name__} com args={args}, kwargs={kwargs}")
        resultado = func(*args, **kwargs)
        logger.debug(f"{func.__name__} retornou: {resultado is not None}")
        return resultado
    return wrapper


@com_retry(tentativas=2)
@com_logging
def requisicao(metodo: str, url: str, dados: Optional[Dict] = None, 
               timeout: int = 120) -> Optional[Dict]:
    """
    Requisição HTTP centralizada (GET/POST)
    
    Args:
        metodo: GET ou POST
        url: URL do endpoint
        dados: Dados JSON (apenas para POST)
        timeout: Timeout em segundos
        
    Returns:
        Resposta JSON ou None em caso de erro
    """
    try:
        kwargs = {"timeout": timeout}
        if dados:
            kwargs["json"] = dados
        
        resp = requests.request(metodo, url, **kwargs)
        return resp.json() if resp.ok else None
    except requests.RequestException as e:
        logger.error(f"Erro na requisição {metodo} {url}: {e}")
        return None


# Funções convenientes
def get(url: str, params: Optional[Dict] = None, timeout: int = 5) -> Optional[Dict]:
    """GET request"""
    url_com_params = f"{url}?{'&'.join(f'{k}={v}' for k,v in params.items())}" if params else url
    return requisicao("GET", url_com_params, timeout=timeout)


def post(url: str, dados: Dict, timeout: int = 120) -> Optional[Dict]:
    """POST request"""
    return requisicao("POST", url, dados, timeout)
