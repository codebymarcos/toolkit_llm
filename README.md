# 🤖 llm_toolkit

**Mini ChatGPT local** - Interface Python para **llama.cpp + Gemma 2B**

## ⚡ Quick Start

```python
# Setup
python llm_toolkit/download.py  # Baixa binário + modelo (~1.6GB)

# Use
from llm_toolkit import gerar_txt
print(gerar_txt("Explique Python em 2 linhas"))
```

## 🎯 Features

✅ **100% Offline** após setup  
✅ **1 função simples**: `gerar_txt(prompt)`  
✅ **Portátil**: funciona em qualquer Windows  
✅ **Rápido**: Gemma 2B Q4 (~3GB RAM)

## ⚠️ Sobre os Binários

**Por que não commitamos `bin/` e `models/`?**

- � **Tamanho**: Modelo = 1.6GB (GitHub limite: 100MB)
- 🔄 **Atualizações**: llama.cpp muda frequentemente  
- 🌐 **Fonte oficial**: Downloads diretos do HuggingFace/GitHub
- 🚀 **Performance**: Usuário baixa a versão mais atual

**Solução**: Script `download.py` automatiza tudo!