"""Core API refatorado - compacto e senior"""

import logging
from functools import lru_cache
from typing import List, Dict, Optional

from .llm import gerar_resposta
from ..client.models import Resposta, RespostaCliente

logger = logging.getLogger(__name__)


class GeradorLLM:
    """Gerador LLM otimizado"""
    
    def __init__(self, temp: float = 0.7, tokens: int = 256):
        self.temp = max(0.0, min(2.0, float(temp)))
        self.tokens = max(1, min(2048, int(tokens)))
        self.historico = []
        logger.info(f"GeradorLLM: temp={self.temp}, tokens={self.tokens}")
    
    @staticmethod
    @lru_cache(maxsize=128)
    def _validar_prompt(prompt: str) -> tuple[bool, Optional[str]]:
        """Valida prompt com cache"""
        if not prompt or not isinstance(prompt, str):
            return False, "Prompt deve ser string não-vazia"
        if len(prompt) > 2000:
            return False, "Prompt muito longo (máx: 2000 chars)"
        return True, None
    
    def gerar(self, prompt: str, temp: Optional[float] = None,
              tokens: Optional[int] = None) -> RespostaCliente:
        """Gera resposta com validação"""
        # Validar
        valido, erro = self._validar_prompt(prompt)
        if not valido:
            logger.error(f"Validação falhou: {erro}")
            return RespostaCliente(sucesso=False, erro=erro)
        
        # Parâmetros
        temp_final = max(0.0, min(2.0, temp)) if temp else self.temp
        tokens_final = max(1, min(2048, tokens)) if tokens else self.tokens
        
        try:
            resposta = gerar_resposta(prompt, temp=temp_final, tokens=tokens_final)
            
            # Verificar erros
            if any(resposta.startswith(x) for x in ["Erro:", "Falta", "Timeout"]):
                return RespostaCliente(sucesso=False, erro=resposta)
            
            # Registrar
            self.historico.append({
                "prompt": prompt,
                "resposta": resposta,
                "temperatura": temp_final,
                "tokens": tokens_final
            })
            
            return RespostaCliente(sucesso=True, dados=resposta)
        except Exception as e:
            logger.error(f"Erro na geração: {e}")
            return RespostaCliente(sucesso=False, erro=str(e)[:100])
    
    def obter_historico(self, ultimos: int = 10) -> List[Dict]:
        """Obtém histórico"""
        return self.historico[-ultimos:]
    
    def limpar_historico(self) -> None:
        """Limpa histórico"""
        self.historico.clear()
        logger.info("Histórico limpo")


# Singleton
_gerador = None

def obter_gerador(temp: float = 0.7, tokens: int = 256) -> GeradorLLM:
    """Obtém instância global"""
    global _gerador
    if _gerador is None:
        _gerador = GeradorLLM(temp=temp, tokens=tokens)
    return _gerador


def resetar_gerador():
    """Reseta instância"""
    global _gerador
    _gerador = None
