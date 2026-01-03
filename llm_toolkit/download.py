"""
Script de download automático - llm_toolkit

Baixa llama.cpp e modelo TinyLlama 1.1B Q4.
"""

import os
import sys
import urllib.request
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).parent
BIN_DIR = BASE_DIR / "bin"
MODELS_DIR = BASE_DIR / "resources" / "models"
PROMPTS_DIR = BASE_DIR / "resources" / "prompts"

# URLs confiáveis
MODEL_URL = "https://huggingface.co/lmstudio-community/gemma-2-2b-it-GGUF/resolve/main/gemma-2-2b-it-Q4_K_M.gguf"

# Lista de URLs de llama.cpp para tentar (do mais recente para o mais antigo)
LLAMA_URLS = [
    "https://github.com/ggerganov/llama.cpp/releases/download/b4344/llama-b4344-bin-win-avx2-x64.zip",
    "https://github.com/ggerganov/llama.cpp/releases/download/b3561/llama-b3561-bin-win-avx2-x64.zip",
    "https://github.com/ggerganov/llama.cpp/releases/download/b3456/llama-b3456-bin-win-avx2-x64.zip",
]


def print_status(text: str, emoji: str = "ℹ️") -> None:
    """Imprime status com emoji."""
    print(f"{emoji} {text}")


def download_with_progress(url: str, dest: Path) -> bool:
    """Baixa arquivo com barra de progresso."""
    try:
        # Garantir que o diretório existe
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        print_status(f"Baixando: {dest.name}", "📥")
        print(f"URL: {url}\n")
        
        def show_progress(block_num, block_size, total_size):
            if total_size > 0:
                downloaded = block_num * block_size
                percent = min(100, downloaded * 100 / total_size)
                mb_down = downloaded / (1024 * 1024)
                mb_total = total_size / (1024 * 1024)
                bar_len = 40
                filled = int(bar_len * percent / 100)
                bar = '█' * filled + '-' * (bar_len - filled)
                print(f'\r[{bar}] {percent:.1f}% ({mb_down:.1f}/{mb_total:.1f} MB)', end='', flush=True)
        
        urllib.request.urlretrieve(url, dest, show_progress)
        print()
        return True
    except KeyboardInterrupt:
        print()
        print_status("Download cancelado pelo usuário", "⚠️")
        if dest.exists():
            dest.unlink()
        return False
    except Exception as e:
        print()
        print_status(f"Erro: {e}", "❌")
        if dest.exists():
            dest.unlink()
        return False


def extract_zip(zip_path: Path, extract_to: Path) -> bool:
    """Extrai ZIP."""
    try:
        print_status("Extraindo...", "📦")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        zip_path.unlink()
        print_status("Extraído", "✅")
        return True
    except Exception as e:
        print_status(f"Erro ao extrair: {e}", "❌")
        return False


def download_llama_cpp() -> bool:
    """Baixa llama.cpp tentando múltiplas URLs."""
    # Garantir que a pasta existe
    BIN_DIR.mkdir(parents=True, exist_ok=True)
    
    llama_exe = BIN_DIR / "llama-cli.exe"
    
    if llama_exe.exists():
        print_status("llama.cpp já instalado", "✅")
        return True
    
    print("\n" + "=" * 60)
    print("📥 PASSO 1: Baixando llama.cpp")
    print("=" * 60)
    
    zip_path = BIN_DIR / "llama.zip"
    
    # Tentar cada URL até conseguir
    for i, url in enumerate(LLAMA_URLS, 1):
        print(f"\n🔄 Tentativa {i}/{len(LLAMA_URLS)}")
        
        if download_with_progress(url, zip_path):
            if extract_zip(zip_path, BIN_DIR):
                # Procurar executável
                found = list(BIN_DIR.rglob("llama-cli.exe"))
                if not found:
                    found = list(BIN_DIR.rglob("llama.exe"))
                    found = [f for f in found if "server" not in f.name.lower()]
                
                if found:
                    import shutil
                    shutil.move(str(found[0]), str(llama_exe))
                    print_status(f"Instalado: {llama_exe}", "✅")
                    return True
                else:
                    print_status("Executável não encontrado no ZIP", "⚠️")
                    continue
        
        # Limpar ZIP se falhou
        if zip_path.exists():
            zip_path.unlink()
    
    # Se todas as tentativas falharem
    print("\n" + "=" * 60)
    print("❌ DOWNLOAD AUTOMÁTICO FALHOU")
    print("=" * 60)
    print("\n📋 DOWNLOAD MANUAL:")
    print("1. Acesse: https://github.com/ggerganov/llama.cpp/releases")
    print("2. Baixe: llama-*-bin-win-avx2-x64.zip (última versão)")
    print("3. Extraia llama-cli.exe ou llama.exe")
    print(f"4. Copie para: {BIN_DIR}")
    print("5. Renomeie para: llama-cli.exe")
    print("\n⚠️  Continuando com download do modelo...\n")
    return False


def download_model() -> bool:
    """Baixa modelo Gemma 2B."""
    # Garantir que a pasta existe
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    model_file = MODELS_DIR / "gemma-2-2b-it-Q4_K_M.gguf"
    
    if model_file.exists():
        print_status("Modelo já baixado", "✅")
        return True
    
    print("\n" + "=" * 60)
    print("📥 PASSO 2: Baixando Gemma 2B Q4 (~1.6GB)")
    print("=" * 60)
    
    if download_with_progress(MODEL_URL, model_file):
        print_status(f"Modelo salvo: {model_file}", "✅")
        return True
    else:
        print("\n📋 DOWNLOAD MANUAL:")
        print("1. Acesse: https://huggingface.co/lmstudio-community/gemma-2-2b-it-GGUF")
        print("2. Baixe: gemma-2-2b-it-Q4_K_M.gguf")
        print(f"3. Salve em: {MODELS_DIR}")
        return False


def main() -> None:
    """Função principal."""
    print("=" * 60)
    print("🚀 Setup llm_toolkit")
    print("=" * 60)
    print("\n📋 Componentes:")
    print("   • llama.cpp (binário Windows)")
    print("   • Gemma 2B Q4 (~1.6GB)")
    print("   • RAM: ~3GB")
    print("=" * 60)
    
    # Criar todas as pastas necessárias
    BIN_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Criar prompt se não existir
    prompt_file = PROMPTS_DIR / "system.txt"
    if not prompt_file.exists():
        prompt_file.write_text("Você é um assistente técnico, educado e objetivo.", encoding="utf-8")
        print_status("Prompt base criado", "✅")
    
    # Download
    llama_ok = download_llama_cpp()
    model_ok = download_model()
    
    # Resumo
    print("\n" + "=" * 60)
    if llama_ok and model_ok:
        print("✅ SETUP COMPLETO!")
        print("=" * 60)
        print("\n🎯 Como usar:")
        print("   from llm_toolkit import gerar_resposta")
        print('   resposta = gerar_resposta("Sua pergunta")')
        print("   print(resposta)")
    else:
        print("⚠️  SETUP INCOMPLETO")
        print("=" * 60)
        if not llama_ok:
            print("❌ llama.cpp: Siga instruções acima")
        if not model_ok:
            print("❌ Modelo: Siga instruções acima")
        print("\nApós baixar manualmente, execute novamente:")
        print("python llm_toolkit/download.py")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
