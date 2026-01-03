"""Biblioteca LLM local - llama.cpp"""

import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent
LLAMA_EXE = BASE_DIR / "bin" / "llama-cli.exe"
MODEL_FILE = BASE_DIR / "models" / "gemma-2-2b-it-Q4_K_M.gguf"
PROMPT_FILE = BASE_DIR / "prompts" / "system.txt"


def gerar_resposta(prompt: str, temp: float = 0.7, tokens: int = 256) -> str:
    """Gera resposta com LLM local - Gemma 2B"""
    
    # Validações rápidas
    if not prompt.strip(): return "Prompt vazio"
    if not LLAMA_EXE.exists(): return "Falta binário: execute download.py"
    if not MODEL_FILE.exists(): return "Falta modelo: execute download.py"
    
    try:
        # Sistema + prompt
        system = PROMPT_FILE.read_text("utf-8").strip() if PROMPT_FILE.exists() else ""
        full_prompt = f"{system}\n\nQ: {prompt.strip()}\nA:"
        
        # Executar llama.cpp
        result = subprocess.run([
            str(LLAMA_EXE), "-m", str(MODEL_FILE), "-p", full_prompt,
            "--temp", str(temp), "-n", str(tokens), "--repeat-penalty", "1.1",
            "--ctx-size", "2048", "--log-disable", "--simple-io"
        ], capture_output=True, text=True, timeout=60, errors='ignore')
        
        if result.returncode != 0:
            return f"Erro: {result.stderr[:100] if result.stderr else 'Erro exec'}"
        
        # Limpar resposta
        resp = (result.stdout or "").strip()
        
        # Remover marcadores comuns
        for mark in ["A:", "Resposta:", "Assistant:", "Q:"]:
            if mark in resp:
                resp = resp.split(mark)[-1].strip()
        
        # Só primeira linha
        resp = resp.split('\n')[0].strip()
        
        return resp or "Resposta vazia"
        
    except subprocess.TimeoutExpired:
        return "Timeout (60s)"
    except Exception as e:
        return f"Erro: {str(e)[:100]}"
