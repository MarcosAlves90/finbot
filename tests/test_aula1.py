"""Testes offline para configurações, fábrica e prompts (sem consumo de LLM)."""
import pytest
from app.config.settings import Settings, MODELOS_PADRAO
from app.llm import fabrica
from app.prompts.catalogo import carregar


def test_modelos_padrao_e_override():
    assert Settings(llm_provedor="groq", _env_file=None).modelo == MODELOS_PADRAO["groq"]
    assert Settings(llm_provedor="gemini", llm_modelo="exemplo", _env_file=None).modelo == "exemplo"


def test_provedor_invalido():
    with pytest.raises(ValueError):
        Settings(llm_provedor="nao-existe", _env_file=None)


def test_chave_nao_vaza_na_representacao():
    assert "segredo-real" not in repr(Settings(groq_api_key="segredo-real", _env_file=None))


def test_chave_ausente_retorna_erro_claro(monkeypatch):
    monkeypatch.setattr(fabrica.settings, "llm_provedor", "groq")
    monkeypatch.setattr(fabrica.settings, "groq_api_key", None)
    with pytest.raises(RuntimeError, match="Defina a chave"):
        fabrica.criar_modelo()


def test_prompt_eh_educacional():
    texto = carregar("sistema").lower()
    assert "não recomendações personalizadas" in texto


def test_prompt_rejeita_path_traversal():
    with pytest.raises(ValueError):
        carregar("../../etc/passwd")
