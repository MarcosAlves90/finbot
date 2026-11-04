"""Chat de terminal da aula 1. Execute com: python -m scripts.chat_terminal."""
from langchain_core.messages import HumanMessage, SystemMessage
from app.config.settings import settings
from app.llm.fabrica import criar_modelo
from app.prompts.catalogo import carregar


def main():
    modelo = criar_modelo()
    mensagens = [SystemMessage(content=carregar("sistema"))]
    print(f"FinBot ({settings.llm_provedor}/{settings.modelo}) — digite sair para encerrar")
    while True:
        try:
            entrada = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if entrada.lower() in {"sair", "exit"}:
            break
        if not entrada:
            continue
        mensagens.append(HumanMessage(content=entrada))
        try:
            resposta = modelo.invoke(mensagens)
        except Exception as erro:
            mensagens.pop()  # não registra uma pergunta que falhou
            print(f"Não foi possível consultar o modelo: {erro}")
            continue
        mensagens.append(resposta)
        uso = resposta.usage_metadata or {}
        print(f"FinBot: {resposta.content}\nTokens entrada: {uso.get('input_tokens', 'n/d')} | saída: {uso.get('output_tokens', 'n/d')}\n")


if __name__ == "__main__":
    main()
