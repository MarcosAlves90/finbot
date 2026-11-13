"""Memória de longo prazo: perfil de cada usuário."""
from app.repository import mongo


def _colecao():
    return mongo.banco()["perfis"]


def salvar_perfil(usuario: str, dados: dict) -> None:
    _colecao().update_one(
        {"usuario": usuario},
        {"$set": {"usuario": usuario, **dados}},
        upsert=True,
    )


def obter_perfil(usuario: str) -> dict:
    return _colecao().find_one({"usuario": usuario}, {"_id": 0}) or {"usuario": usuario}


def texto_perfil(usuario: str) -> str:
    perfil = obter_perfil(usuario)
    campos = ("nome", "objetivo", "experiencia")
    return "; ".join(f"{campo}: {perfil[campo]}" for campo in campos if perfil.get(campo)) or "não informado"
