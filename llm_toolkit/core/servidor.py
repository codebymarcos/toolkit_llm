"""Servidor Flask compacto com blueprints"""

import logging
from flask import Flask, request, jsonify, Blueprint

from ..api import obter_gerador
from ..config import config

logger = logging.getLogger(__name__)

# Blueprint para endpoints
bp = Blueprint('llm', __name__)


@bp.route('/health', methods=['GET'])
def health():
    """Verificação de saúde"""
    return jsonify({"status": "ok", "versao": "1.0.0"}), 200


@bp.route('/gerar', methods=['POST'])
def gerar():
    """Gera resposta"""
    dados = request.get_json() or {}
    prompt = dados.get("prompt")
    
    if not prompt:
        return jsonify({"sucesso": False, "erro": "Campo 'prompt' obrigatório"}), 400
    
    gerador = obter_gerador()
    resposta = gerador.gerar(
        prompt,
        temp=dados.get("temperatura"),
        tokens=dados.get("tokens")
    )
    
    status = 200 if resposta.sucesso else 400
    return jsonify(resposta.para_dict()), status


@bp.route('/gerar-multiplo', methods=['POST'])
def gerar_multiplo():
    """Gera múltiplas respostas"""
    dados = request.get_json() or {}
    prompts = dados.get("prompts", [])
    
    if not prompts or not isinstance(prompts, list):
        return jsonify({"sucesso": False, "erro": "'prompts' deve ser lista"}), 400
    
    gerador = obter_gerador()
    resultados = [gerador.gerar(p, dados.get("temperatura"), dados.get("tokens")).para_dict() for p in prompts]
    
    return jsonify({"sucesso": True, "dados": resultados, "total": len(resultados)}), 200


@bp.route('/historico', methods=['GET'])
def historico():
    """Obtém histórico"""
    ultimos = request.args.get('ultimos', 10, type=int)
    hist = obter_gerador().obter_historico(ultimos)
    return jsonify({"sucesso": True, "dados": hist, "total": len(hist)}), 200


@bp.route('/limpar-historico', methods=['POST'])
def limpar_historico():
    """Limpa histórico"""
    obter_gerador().limpar_historico()
    return jsonify({"sucesso": True, "mensagem": "Histórico limpo"}), 200


@bp.errorhandler(404)
def nao_encontrado(e):
    return jsonify({"sucesso": False, "erro": "Endpoint não encontrado"}), 404


@bp.errorhandler(500)
def erro_interno(e):
    logger.error(f"Erro 500: {e}")
    return jsonify({"sucesso": False, "erro": "Erro interno"}), 500


def criar_app():
    """Factory pattern para criar app"""
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    app.register_blueprint(bp)
    return app


app = criar_app()


def iniciar_servidor(host: str = None, porta: int = None, debug: bool = False):
    """Inicia servidor com config"""
    host = host or config.api.host
    porta = porta or config.api.porta
    debug = debug or config.api.debug
    
    logger.info(f"Servidor em {host}:{porta} (debug={debug})")
    app.run(host=host, port=porta, debug=debug)


if __name__ == '__main__':
    iniciar_servidor(debug=True)
