"""Seleção do provedor de LLM sem acoplar o restante da aplicação a um SDK."""
from app.config.settings import settings


def _chave(segredo):
    valor = segredo.get_secret_value() if segredo else ""
    if not valor:
        raise RuntimeError(f"Defina a chave do provedor '{settings.llm_provedor}' no .env")
    return valor


def criar_modelo(temperatura: float = 0.3):
    if not 0.0 <= temperatura <= 2.0:
        raise ValueError("Temperatura fora do intervalo [0, 2]")
    if settings.llm_provedor == "groq":
        chave = _chave(settings.groq_api_key)
        from langchain_groq import ChatGroq
        return ChatGroq(model=settings.modelo, temperature=temperatura, api_key=chave)
    if settings.llm_provedor == "gemini":
        chave = _chave(settings.gemini_api_key)
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=settings.modelo, temperature=temperatura, google_api_key=chave)
    if settings.llm_provedor == "mistral":
        chave = _chave(settings.mistral_api_key)
        from langchain_mistralai import ChatMistralAI
        return ChatMistralAI(model=settings.modelo, temperature=temperatura, api_key=chave)
    raise ValueError("Provedor de LLM desconhecido")
