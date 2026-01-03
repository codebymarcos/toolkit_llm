"""Configuração de dependências para distribuição"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="llm-toolkit",
    version="1.0.0",
    author="Marco",
    description="Chat LLM Local - Interface Python para llama.cpp + Gemma 2B",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.8",
    install_requires=[
        "flask>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "llm-servidor=llm_toolkit.cli:main",
        ],
    },
)
