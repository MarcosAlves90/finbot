"""Aulas 4 e 5: um AGENTE ÚNICO com ferramentas (pensar ⇄ ferramentas), ver app/agents/base.py."""
from functools import lru_cache
from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.graph.message import add_messages

from app.agents.base import criar_agente, fontes_do_turno
from app.agents.chatbot import no_chatbot
from app.llm.observabilidade import callbacks, rastrear
from app.repository import checkpointer, conversas, perfis
from app.tools.mercado import FERRAMENTAS_MERCADO
from app.utils.mensagens import conversa_limpa


class EstadoChat(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], add_messages]
    perfil: str
    passos: int


def montar_grafo(memoria=None):
    # O grafo agora é o agente com ferramentas (o loop pensar ⇄ ferramentas de base.py).
    return criar_agente("finbot", "sistema", FERRAMENTAS_MERCADO, checkpointer=memoria)


@lru_cache

def grafo():
    return montar_grafo(checkpointer.criar_checkpointer())


def executar(pergunta: str, sessao: str, usuario: str = "anonimo") -> dict:
    config = {"configurable": {"thread_id": sessao}, "callbacks": callbacks()}
    entrada = {"messages": [HumanMessage(pergunta)], "perfil": perfis.texto_perfil(usuario), "passos": 0}
    with rastrear(sessao, usuario):
        estado = grafo().invoke(entrada, config)
    conversas.registrar(sessao, usuario, pergunta)
    final = estado["messages"][-1]
    # Posição da última pergunta do usuário: as fontes são só deste turno.
    ultima_pergunta = max(i for i, mensagem in enumerate(estado["messages"]) if isinstance(mensagem, HumanMessage))
    fontes = fontes_do_turno(estado["messages"][ultima_pergunta:])
    return {"resposta": final.content, "agente": "finbot", "fontes": fontes}


def historico(sessao: str) -> list[dict]:
    estado = grafo().get_state({"configurable": {"thread_id": sessao}})
    mensagens = estado.values.get("messages", []) if estado else []
    return [
        {"papel": "user" if mensagem.type == "human" else "assistant",
         "conteudo": mensagem.content, "agente": mensagem.name}
        for mensagem in conversa_limpa(mensagens, limite=1000)
    ]


if __name__ == "__main__":
    print(montar_grafo().get_graph(xray=True).draw_mermaid())
