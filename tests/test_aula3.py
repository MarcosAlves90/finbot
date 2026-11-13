from app.agents import grafo
from app.prompts import catalogo
from app.repository import perfis


def test_memoria_de_curto_prazo_por_sessao(falso):
    grafo.executar("Meu nome é Ana", sessao="t1")
    grafo.executar("Qual é meu nome?", sessao="t1")
    assert "Meu nome é Ana" in [m.content for m in falso.vistas]

    grafo.executar("Oi", sessao="t2")
    assert "Meu nome é Ana" not in [m.content for m in falso.vistas]


def test_historico_vem_do_checkpointer(falso):
    grafo.executar("Pergunta 1", sessao="t3")
    assert [m["papel"] for m in grafo.historico("t3")] == ["user", "assistant"]


def test_perfil_entra_no_prompt(falso):
    perfis.salvar_perfil("bia", {"nome": "Bia", "objetivo": "reserva de emergência"})
    grafo.executar("Oi", sessao="t4", usuario="bia")
    assert "reserva de emergência" in falso.vistas[0].content


def test_prompt_sem_langfuse_usa_arquivo_local():
    prompt = catalogo.obter("sistema")
    assert prompt.is_fallback
    assert prompt.compile(perfil="iniciante").endswith("iniciante")


def test_api_perfil_e_conversas(api):
    api.put("/usuarios/caio/perfil", json={"nome": "Caio", "experiencia": "iniciante"})
    assert api.get("/usuarios/caio/perfil").json()["nome"] == "Caio"
    api.post("/chat", json={"mensagem": "O que é CDI?", "sessao": "c1", "usuario": "caio"})
    assert api.get("/usuarios/caio/conversas").json()[0]["titulo"] == "O que é CDI?"
