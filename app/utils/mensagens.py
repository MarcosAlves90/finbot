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


def turno_atual(mensagens: list[AnyMessage], limite: int = 10) -> list[AnyMessage]:
    """Histórico limpo + TUDO desde a última pergunta (inclusive chamadas de ferramenta deste turno)."""
    # Posição da última pergunta (0 se não houver nenhuma).
    ultima = max((i for i, mensagem in enumerate(mensagens) if isinstance(mensagem, HumanMessage)), default=0)
    # Antes da pergunta: só a conversa limpa. Depois dela: tudo, para o agente ver os resultados das ferramentas.
    return conversa_limpa(mensagens[:ultima], limite) + list(mensagens[ultima:])
