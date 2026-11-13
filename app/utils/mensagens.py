"""Seleciona mensagens úteis para o contexto do modelo e para a tela."""
from langchain_core.messages import AIMessage, AnyMessage, HumanMessage


def conversa_limpa(mensagens: list[AnyMessage], limite: int = 10) -> list[AnyMessage]:
    limpas = [
        mensagem
        for mensagem in mensagens
        if isinstance(mensagem, HumanMessage)
        or (isinstance(mensagem, AIMessage) and mensagem.content and not mensagem.tool_calls)
    ]
    return limpas[-limite:]
