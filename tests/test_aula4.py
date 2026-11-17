"""Aula 4 — ferramentas e o loop de tool-calling."""
from pathlib import Path
from unittest.mock import Mock

from pydantic import SecretStr

from app.config.settings import Settings, settings


def test_settings_de_mercado_e_limite_de_passos():
    config = Settings(_env_file=None, brapi_token="token-falso", max_passos_agente=1)
    assert config.brapi_token.get_secret_value() == "token-falso"
    assert config.max_passos_agente == 1


def test_render_declara_token_brapi_secreto():
    yaml = (Path(__file__).parents[1] / "render.yaml").read_text()
    assert "- key: BRAPI_TOKEN\n        sync: false" in yaml


def test_get_json_aplica_cabecalho_timeout_e_token_apenas_brapi(monkeypatch):
    arquivo = Path(__file__).parents[1] / "app/utils/http.py"
    assert arquivo.is_file(), "a camada HTTP da Aula 4 ainda não existe"

    import requests

    from app.utils.http import get_json

    chamada = Mock()
    chamada.return_value.raise_for_status.return_value = None
    chamada.return_value.json.return_value = {"ok": True}
    monkeypatch.setattr(requests, "get", chamada)
    monkeypatch.setattr(settings, "brapi_token", SecretStr("token-falso-de-teste"))

    assert get_json("https://brapi.dev/api/v2/stocks/quote", {"symbols": "PETR4"}) == {"ok": True}
    assert chamada.call_args.kwargs == {
        "params": {"symbols": "PETR4"},
        "headers": {"User-Agent": "FinBot-FATEC/1.0", "Authorization": "Bearer token-falso-de-teste"},
        "timeout": 15,
    }

    chamada.reset_mock()
    get_json("https://api.bcb.gov.br/dados")
    assert chamada.call_args.kwargs["headers"] == {"User-Agent": "FinBot-FATEC/1.0"}


def mercado():
    arquivo = Path(__file__).parents[1] / "app/tools/mercado.py"
    assert arquivo.is_file(), "as ferramentas de mercado da Aula 4 ainda não existem"
    from app.tools import mercado as modulo
    return modulo


# O LLM escolhe a ferramenta pela descrição: ela precisa ser longa e clara.
def test_ferramentas_tem_descricao_e_argumentos():
    m = mercado()
    for ferramenta in m.FERRAMENTAS_MERCADO:
        assert len(ferramenta.description) > 80, f"descrição curta demais em {ferramenta.name}"
    assert "não use para explicar conceitos" in m.indicadores_economicos.description.lower()
    assert m.cotacao_acao.args["ticker"]["type"] == "string"


# As ferramentas leem e convertem os dados das APIs (aqui, respostas falsas).
def test_ferramenta_le_api(falso):
    m = mercado()
    assert m.indicadores_economicos.invoke({})["cdi_aa"]["valor"] == 14.9
    assert m.cotacao_acao.invoke({"ticker": "petr4"})["preco"] == 38.45
    assert m.indicadores_fii.invoke({"ticker": "MXRF11"})["dividend_yield_12m_pct"] == 12.4


# Se a API cair, a ferramenta devolve {"erro": ...} em vez de quebrar.
def test_ferramenta_nao_quebra_se_api_falhar(falso, monkeypatch):
    def sem_internet(*args, **kwargs):
        raise ConnectionError("sem internet")

    m = mercado()
    monkeypatch.setattr(m, "get_json", sem_internet)
    assert "erro" in m.indicadores_economicos.invoke({})


def test_taxas_pedem_dados_ate_hoje(falso, monkeypatch):
    """A meta Selic vinha com data futura; agora pedimos o período até hoje."""
    from datetime import date

    pedidos = []

    def registra(url, params=None):
        pedidos.append(params)
        return [{"data": "21/10/2026", "valor": "15.00"}]

    m = mercado()
    monkeypatch.setattr(m, "get_json", registra)
    m.buscar_taxas()
    assert pedidos[0]["dataFinal"] == date.today().strftime("%d/%m/%Y")


def test_guardrail_limita_as_voltas(falso, monkeypatch):
    """Com limite de 1 passo, o agente pede a ferramenta e o código o interrompe."""
    arquivo = Path(__file__).parents[1] / "app/agents/base.py"
    assert arquivo.is_file(), "o motor de agentes da Aula 4 ainda não existe"
    from langchain_core.messages import HumanMessage
    from app.agents.base import criar_agente
    m = mercado()
    monkeypatch.setattr(settings, "max_passos_agente", 1)
    agente = criar_agente("teste", "sistema", m.FERRAMENTAS_MERCADO)
    saida = agente.invoke({"messages": [HumanMessage("Selic?")]})
    assert "poucos passos" in saida["messages"][-1].content


def test_nome_de_ferramenta_inventado_tenta_de_novo(falso, monkeypatch):
    """Simula o erro real do Groq: 'attempted to call tool taxa_bcb which was not in request.tools'."""
    arquivo = Path(__file__).parents[1] / "app/agents/base.py"
    assert arquivo.is_file(), "o motor de agentes da Aula 4 ainda não existe"
    original = falso.invoke
    falhas = {"n": 0}

    def invoke_com_erro(self, mensagens, config=None):
        if falhas["n"] == 0 and getattr(self, "_ferramentas", None):
            falhas["n"] += 1
            raise RuntimeError("Error code: 400 - tool call validation failed: attempted to call tool 'taxa_bcb'")
        return original.__func__(self, mensagens, config)

    monkeypatch.setattr(type(falso), "invoke", invoke_com_erro)
    from langchain_core.messages import HumanMessage
    from app.agents.base import criar_agente
    m = mercado()
    agente = criar_agente("teste", "sistema", m.FERRAMENTAS_MERCADO)
    saida = agente.invoke({"messages": [HumanMessage("Selic?")]})
    assert falhas["n"] == 1
    assert "tool:indicadores_economicos" in falso.chamadas
    assert saida["messages"][-1].content.startswith("resposta de teste")


def test_regra_no_prompt_exige_ferramenta_para_dados_atuais():
    from app.prompts import catalogo
    assert "Para qualquer valor ATUAL" in catalogo.carregar("sistema")


def test_turno_atual_preserva_resultados_de_ferramenta():
    from app.utils import mensagens
    assert hasattr(mensagens, "turno_atual"), "turno_atual ainda não existe"
    from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

    chamada = AIMessage(content="", tool_calls=[{"name": "cotacao_acao", "args": {"ticker": "PETR4"}, "id": "c1"}])
    resultado = ToolMessage(content='{"preco": 38.45}', tool_call_id="c1")
    mensagens_turno = [HumanMessage("antes"), AIMessage("resposta anterior"), HumanMessage("agora"), chamada, resultado]
    assert mensagens.turno_atual(mensagens_turno) == mensagens_turno


# O modelo pede a ferramenta, recebe o dado e responde com ele, citando a fonte.
def test_loop_pede_ferramenta_e_responde_com_o_dado(falso):
    from app.agents import grafo

    falso.ferramenta = "cotacao_acao"
    saida = grafo.executar("Quanto está a PETR4?", sessao="aula4-m1")
    assert falso.chamadas == ["tool:cotacao_acao", "resposta"]
    assert "38.45" in saida["resposta"]
    assert saida["fontes"] == ["brapi.dev"]


def test_janela_contexto_preserva_ciclo_de_ferramenta_e_historico(api, falso, monkeypatch):
    """O turno atual mantém pedidos/resultados de ferramentas e o histórico completo persiste."""
    from app.utils.mensagens import conversa_limpa

    contextos = []
    invoke_original = type(falso).invoke

    def capturar_contexto(self, mensagens, config=None):
        contextos.append(list(mensagens))
        return invoke_original(self, mensagens, config)

    monkeypatch.setattr(type(falso), "invoke", capturar_contexto)
    sessao = "limite-contexto-tools"
    perguntas = [f"pergunta interação {i}" for i in range(1, 13)]

    for pergunta in perguntas:
        resposta = api.post("/chat", json={"mensagem": pergunta, "sessao": sessao})
        assert resposta.status_code == 200

    assert len(contextos) == 24
    for turno, pergunta in enumerate(perguntas):
        primeira_chamada = contextos[turno * 2]
        textos = [mensagem.content for mensagem in primeira_chamada]
        assert pergunta in textos
        assert len(conversa_limpa(primeira_chamada[1:], limite=1000)) <= 11

    textos_7 = [mensagem.content for mensagem in contextos[12]]
    assert perguntas[0] not in textos_7
    assert perguntas[1] in textos_7
    assert perguntas[2] in textos_7
    assert perguntas[6] in textos_7
    textos_12 = [mensagem.content for mensagem in contextos[22]]
    assert perguntas[5] not in textos_12
    assert perguntas[6] in textos_12
    assert perguntas[11] in textos_12

    historico = api.get(f"/sessoes/{sessao}/mensagens").json()
    assert len(historico) == 24
    assert [mensagem["conteudo"] for mensagem in historico if mensagem["papel"] == "user"] == perguntas
