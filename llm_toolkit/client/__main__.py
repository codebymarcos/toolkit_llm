"""Cliente interativo para API LLM"""

import sys
from .api import ClienteAPI


def main():
    """Função principal do cliente"""
    cliente = ClienteAPI()
    
    # Verificar disponibilidade
    if not cliente.verificar_saude():
        print("Erro: API não está disponível")
        print("Rode o servidor: python -m llm_toolkit.scripts.rodar_servidor")
        sys.exit(1)
    
    print("API LLM disponível!")
    print("=" * 50)
    
    # Teste simples
    resposta = cliente.gerar("Qual é a capital da França?")
    if resposta.sucesso:
        print(f"Resposta: {resposta.dados}")
    else:
        print(f"Erro: {resposta.erro}")


if __name__ == "__main__":
    main()
