"""Agente de conversa geral como nó do grafo."""
from langchain_core.messages import AIMessage, SystemMessage

from app.llm import fabrica
from app.llm.observabilidade import config_prompt
from app.prompts import catalogo
from app.utils.mensagens import conversa_limpa


def no_chatbot(estado: dict) -> dict:
    prompt = catalogo.obter("sistema")
    sistema = SystemMessage(prompt.compile(perfil=estado.get("perfil", "não informado")))
    resposta = fabrica.criar_modelo().invoke(
        [sistema] + conversa_limpa(estado["messages"]),
        config=config_prompt(prompt),
    )
    return {"messages": [AIMessage(content=resposta.content, name="conversa")]}
