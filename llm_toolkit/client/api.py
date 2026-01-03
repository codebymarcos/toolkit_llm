"""Cliente REST compacto e eficiente"""

from typing import List, Dict
from .models import RespostaCliente
from .http import get, post


class ClienteAPI:
    """Cliente minimalista para API REST"""
    
    def __init__(self, url_base: str = "http://127.0.0.1:5000"):
        self.url_base = url_base.rstrip('/')
    
    def _chamada(self, endpoint: str, metodo: str = "GET", 
                 dados: Dict = None, timeout: int = 120) -> RespostaCliente:
        """Chamada genérica (DRY)"""
        url = f"{self.url_base}{endpoint}"
        resposta_json = (
            post(url, dados, timeout) if metodo == "POST" 
            else get(url, dados, timeout)
        )
        
        if not resposta_json:
            return RespostaCliente(sucesso=False, erro="Falha na requisição")
        
        return RespostaCliente(
            sucesso=resposta_json.get('sucesso', False),
            dados=resposta_json.get('dados'),
            erro=resposta_json.get('erro'),
            timestamp=resposta_json.get('timestamp')
        )
    
    def verificar_saude(self) -> bool:
        """Verifica disponibilidade"""
        resposta = self._chamada("/health", timeout=5)
        return resposta.sucesso
    
    def gerar(self, prompt: str, temperatura: float = 0.7, 
              tokens: int = 256) -> RespostaCliente:
        """Gera resposta"""
        return self._chamada(
            "/gerar",
            "POST",
            {"prompt": prompt, "temperatura": temperatura, "tokens": tokens}
        )
    
    def gerar_multiplo(self, prompts: List[str], temperatura: float = 0.7,
                       tokens: int = 256) -> List[RespostaCliente]:
        """Gera múltiplas respostas"""
        resposta = self._chamada(
            "/gerar-multiplo",
            "POST",
            {"prompts": prompts, "temperatura": temperatura, "tokens": tokens},
            timeout=300
        )
        
        if not resposta.sucesso:
            return [resposta]
        
        # Parse da resposta formatada
        try:
            import json
            dados = json.loads(resposta.dados) if isinstance(resposta.dados, str) else resposta.dados
            return [RespostaCliente(**item) for item in dados] if isinstance(dados, list) else [resposta]
        except:
            return [resposta]
    
    def obter_historico(self, ultimos: int = 10) -> List[Dict]:
        """Obtém histórico"""
        resposta = self._chamada("/historico", "GET", {"ultimos": ultimos}, timeout=5)
        return resposta.dados if resposta.sucesso else []
    
    def limpar_historico(self) -> bool:
        """Limpa histórico"""
        resposta = self._chamada("/limpar-historico", "POST", timeout=5)
        return resposta.sucesso


if __name__ == "__main__":
    cliente = ClienteAPI()
    
    if not cliente.verificar_saude():
        print("Erro: API não está disponível")
        print("Rode: python -m llm_toolkit.scripts.rodar_servidor")
        exit(1)
    
    print("API disponível!")
    resposta = cliente.gerar("Qual é a capital da França?")
    print(f"Resposta: {resposta.dados}" if resposta.sucesso else f"Erro: {resposta.erro}")
