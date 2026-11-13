"""Publica os prompts locais no Langfuse.

Uso: python -m scripts.publicar_prompts [--forcar]
"""
import sys

from app.config.settings import settings
from app.llm.observabilidade import cliente_langfuse
from app.prompts import catalogo


def publicar(forcar: bool = False) -> None:
    if not settings.langfuse_ativo:
        print("Configure LANGFUSE_PUBLIC_KEY e LANGFUSE_SECRET_KEY no .env primeiro.")
        return

    cliente = cliente_langfuse()
    for nome in catalogo.nomes_locais():
        texto = catalogo.carregar(nome)
        remoto = catalogo.nome_langfuse(nome)
        try:
            atual = cliente.get_prompt(remoto, label="production", cache_ttl_seconds=0)
            if not forcar or atual.prompt == texto:
                print(f"=  {remoto}: já existe (versão {atual.version})")
                continue
        except Exception:
            pass
        novo = cliente.create_prompt(
            name=remoto,
            prompt=texto,
            labels=["production"],
            commit_message="enviado por scripts/publicar_prompts.py",
        )
        print(f"+  {remoto}: versão {novo.version} (production)")
    cliente.flush()


if __name__ == "__main__":
    publicar(forcar="--forcar" in sys.argv)
