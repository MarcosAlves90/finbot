# app/prompts/catalogo.py
"""Catálogo de prompts.

Cada prompt é um arquivo .md nesta pasta (ex.: sistema.md). Prompt é ARTEFATO, não texto solto no código.

Aula 3: o Langfuse passa a ser a fonte da verdade. O arquivo .md é a semente para publicação e a reserva local se o Langfuse ficar indisponível.
"""
from pathlib import Path

from app.config.settings import settings

PASTA = Path(__file__).parent


def carregar(nome: str) -> str:
    """Lê o texto do prompt local (arquivo app/prompts/<nome>.md)."""
    return (PASTA / f"{nome}.md").read_text(encoding="utf-8").strip()


def nomes_locais() -> list[str]:
    return sorted(arquivo.stem for arquivo in PASTA.glob("*.md"))


def nome_langfuse(nome: str) -> str:
    return f"finbot-{nome}"


class PromptLocal:
    is_fallback = True
    version = "local"

    def __init__(self, texto: str):
        self.prompt = texto

    def compile(self, **variaveis) -> str:
        texto = self.prompt
        for chave, valor in variaveis.items():
            texto = texto.replace("{{" + chave + "}}", str(valor))
        return texto


def obter(nome: str):
    local = carregar(nome)
    if not settings.langfuse_ativo:
        return PromptLocal(local)
    try:
        from app.llm.observabilidade import cliente_langfuse

        return cliente_langfuse().get_prompt(
            nome_langfuse(nome), label="production", fallback=local, cache_ttl_seconds=60
        )
    except Exception as erro:
        print(f"[prompts] Langfuse indisponível ({erro}); usando {nome}.md")
        return PromptLocal(local)
