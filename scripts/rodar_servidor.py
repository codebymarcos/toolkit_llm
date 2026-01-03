"""CLI para iniciar servidor"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from llm_toolkit.core.servidor import iniciar_servidor


def main():
    """Parse argumentos e inicia servidor"""
    parser = argparse.ArgumentParser(description='Servidor API REST LLM')
    parser.add_argument('--host', default='127.0.0.1', help='Host (padrão: 127.0.0.1)')
    parser.add_argument('--porta', type=int, default=5000, help='Porta (padrão: 5000)')
    parser.add_argument('--debug', action='store_true', help='Modo debug')
    parser.add_argument('--publico', action='store_true', help='Permitir externo (0.0.0.0)')
    
    args = parser.parse_args()
    host = '0.0.0.0' if args.publico else args.host
    
    print(f"\nServidorAPI REST - LLM Local")
    print(f"{'='*50}")
    print(f"Host: {host}:{args.porta} | Debug: {args.debug}")
    print(f"Endpoints: /health /gerar /gerar-multiplo /historico /limpar-historico")
    print(f"{'='*50}\n")
    
    iniciar_servidor(host=host, porta=args.porta, debug=args.debug)


if __name__ == '__main__':
    main()

