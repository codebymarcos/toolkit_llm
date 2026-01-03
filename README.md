# llm_toolkit

**Chat LLM Local** - Interface Python para **llama.cpp + Gemma 2B**

## Quick Start

```python
# Setup
python llm_toolkit/download.py  # Baixa binário + modelo (~1.6GB)

# Use
from llm_toolkit import gerar_resposta
print(gerar_resposta("Explique Python em 2 linhas"))
```

## Features

- **100% Offline** após setup  
- **1 função simples**: `gerar_resposta(prompt)`  
- **Portátil**: funciona em qualquer Windows  
- **Eficiente**: Gemma 2B Q4 (~3GB RAM)

## Configuração dos Binários

**Por que `bin/` e `models/` não estão commitados?**

- **Tamanho**: Modelo = 1.6GB (limite do GitHub: 100MB)
- **Atualizações**: llama.cpp evolui frequentemente  
- **Fonte oficial**: Downloads diretos do HuggingFace/GitHub
- **Portabilidade**: Usuário obtém a versão mais atual

**Solução**: Script `download.py` automatiza todo o processo