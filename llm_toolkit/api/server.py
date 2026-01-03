"""API Server - Geração de respostas LLM"""

from functools import lru_cache
from typing import List, Dict, Optional
import logging

from ..core.llm import gerar_resposta
from ..client.models import RespostaCliente
from ..constantes import *

logger = logging.getLogger(__name__)


class GeradorLLM:
    """Gerador LLM otimizado com cache e validação"""
    
    def __init__(self, temp: float = 0.7, tokens: int = 256):
        self.temp = max(TEMPERATURA_MIN, min(TEMPERATURA_MAX, float(temp)))
        self.tokens = max(TOKEN_MIN, min(TOKEN_MAX, int(tokens)))
        self.historico = []
        logger.info(f"GeradorLLM: temp={self.temp}, tokens={self.tokens}")
    
    @staticmethod
    @lru_cache(maxsize=128)
    def _validar_prompt(prompt: str) -> tuple[bool, Optional[str]]:
        """Valida prompt com cache"""
        if not prompt or not isinstance(prompt, str):
            return False, ERRO_PROMPT_VAZIO
        if len(prompt) > PROMPT_MAX_LENGTH:
            return False, ERRO_PROMPT_LONGO
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
        temp_final = max(TEMPERATURA_MIN, min(TEMPERATURA_MAX, temp)) if temp else self.temp
        tokens_final = max(TOKEN_MIN, min(TOKEN_MAX, tokens)) if tokens else self.tokens
        
        try:
            logger.info(LOG_GERACAO_INICIADA.format(prompt=prompt[:50]))
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
            
            logger.info(LOG_GERACAO_SUCESSO)
            return RespostaCliente(sucesso=True, dados=resposta)
        except Exception as e:
            logger.error(LOG_GERACAO_ERRO.format(erro=e))
            return RespostaCliente(sucesso=False, erro=str(e)[:100])
    
    def obter_historico(self, ultimos: int = HISTORICO_PADRAO) -> List[Dict]:
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
