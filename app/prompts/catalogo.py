"""Carrega prompts versionados como arquivos Markdown."""
from pathlib import Path

PASTA = Path(__file__).parent


def carregar(nome: str) -> str:
    if not nome.isidentifier():
        raise ValueError("Nome de prompt inválido")
    return (PASTA / f"{nome}.md").read_text(encoding="utf-8").strip()
