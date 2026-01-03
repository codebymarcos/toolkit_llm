"""Constantes e padrões da aplicação"""

# Limites
PROMPT_MAX_LENGTH = 2000
TOKEN_MIN = 1
TOKEN_MAX = 2048
TEMPERATURA_MIN = 0.0
TEMPERATURA_MAX = 2.0
TIMEOUT_PADRAO = 120

# Valores padrão
TEMPERATURA_PADRAO = 0.7
TOKENS_PADRAO = 256
HISTORICO_PADRAO = 10
RETRY_TENTATIVAS = 3

# Endpoints
ENDPOINT_HEALTH = "/health"
ENDPOINT_GERAR = "/gerar"
ENDPOINT_GERAR_MULTIPLO = "/gerar-multiplo"
ENDPOINT_HISTORICO = "/historico"
ENDPOINT_LIMPAR = "/limpar-historico"

# Mensagens de erro
ERRO_PROMPT_VAZIO = "Prompt deve ser string não-vazia"
ERRO_PROMPT_LONGO = f"Prompt muito longo (máx: {PROMPT_MAX_LENGTH} caracteres)"
ERRO_API_INDISPONIVEL = "API não está disponível"
ERRO_REQUISICAO = "Falha na requisição"

# Logs
LOG_API_START = "Iniciando API em {host}:{porta}"
LOG_GERACAO_INICIADA = "Processando: '{prompt}'"
LOG_GERACAO_SUCESSO = "Resposta gerada com sucesso"
LOG_GERACAO_ERRO = "Falha na geração: {erro}"
