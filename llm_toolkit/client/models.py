"""Modelos compartilhados"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class Resposta(ABC):
    """Interface base para respostas"""
    sucesso: bool
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
    
    def para_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return asdict(self)


@dataclass
class RespostaCliente(Resposta):
    """Resposta do cliente HTTP"""
    dados: Optional[str] = None
    erro: Optional[str] = None
