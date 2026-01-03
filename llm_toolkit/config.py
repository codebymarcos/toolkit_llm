"""Configuração centralizada do projeto com suporte a .env"""

import os
from pathlib import Path
from dataclasses import dataclass


def _env(chave: str, tipo: type = str, padrao=None):
    """Obtém valor de variável de ambiente com tipo"""
    valor = os.getenv(chave, padrao)
    if valor is None:
        return padrao
    if tipo == bool:
        return valor.lower() in ('true', '1', 'yes', 'on')
    if tipo == int:
        return int(valor)
    if tipo == float:
        return float(valor)
    return valor


@dataclass
class ConfigAPI:
    """Configuração da API"""
    host: str = None
    porta: int = None
    debug: bool = None
    timeout_padrao: int = None
    
    def __post_init__(self):
        """Carrega valores de ambiente com fallback"""
        self.host = self.host or _env("API_HOST", str, "127.0.0.1")
        self.porta = self.porta or _env("API_PORTA", int, 5000)
        self.debug = self.debug if self.debug is not None else _env("API_DEBUG", bool, False)
        self.timeout_padrao = self.timeout_padrao or _env("API_TIMEOUT", int, 120)
    
    @property
    def url_base(self) -> str:
        """URL base da API"""
        return f"http://{self.host}:{self.porta}"


@dataclass
class ConfigLLM:
    """Configuração do LLM"""
    temperatura: float = None
    tokens: int = None
    timeout: int = None
    
    def __post_init__(self):
        """Carrega valores de ambiente com fallback"""
        self.temperatura = self.temperatura or _env("LLM_TEMPERATURA", float, 0.7)
        self.tokens = self.tokens or _env("LLM_TOKENS", int, 256)
        self.timeout = self.timeout or _env("LLM_TIMEOUT", int, 60)
        self.validar()
    
    def validar(self) -> None:
        """Valida os parâmetros"""
        if not 0.0 <= self.temperatura <= 2.0:
            raise ValueError("Temperatura deve estar entre 0.0 e 2.0")
        if not 1 <= self.tokens <= 2048:
            raise ValueError("Tokens deve estar entre 1 e 2048")


@dataclass
class ConfigCliente:
    """Configuração do cliente"""
    url_base: str = None
    timeout: int = None
    retry_tentativas: int = None
    
    def __post_init__(self):
        """Carrega valores de ambiente com fallback"""
        self.url_base = self.url_base or _env("CLIENTE_URL_BASE", str, "http://127.0.0.1:5000")
        self.timeout = self.timeout or _env("CLIENTE_TIMEOUT", int, 120)
        self.retry_tentativas = self.retry_tentativas or _env("CLIENTE_RETRY_TENTATIVAS", int, 3)


@dataclass
class ConfigApp:
    """Configuração geral da aplicação"""
    api: ConfigAPI = None
    llm: ConfigLLM = None
    cliente: ConfigCliente = None
    
    def __post_init__(self):
        if self.api is None:
            self.api = ConfigAPI()
        if self.llm is None:
            self.llm = ConfigLLM()
        if self.cliente is None:
            self.cliente = ConfigCliente()


# Instância global
config = ConfigApp()
