from app.repository import conversas, mongo, perfis


def test_perfil_salva_lê_e_formata_campos(monkeypatch):
    import mongomock

    banco = mongomock.MongoClient().finbot_teste
    monkeypatch.setattr(mongo, "banco", lambda: banco)

    perfis.salvar_perfil("bia", {"nome": "Bia", "objetivo": "reserva"})

    assert perfis.obter_perfil("bia")["nome"] == "Bia"
    assert perfis.texto_perfil("bia") == "nome: Bia; objetivo: reserva"
    assert perfis.texto_perfil("desconhecida") == "não informado"


def test_conversa_registra_titulo_inicial_e_lista_por_usuario(monkeypatch):
    import mongomock

    banco = mongomock.MongoClient().finbot_teste
    monkeypatch.setattr(mongo, "banco", lambda: banco)

    conversas.registrar("s1", "bia", "Pergunta original")
    conversas.registrar("s1", "bia", "Pergunta seguinte")
    conversas.registrar("s2", "caio", "Outra conversa")

    assert [item["titulo"] for item in conversas.listar("bia")] == ["Pergunta original"]
    assert conversas.listar("caio")[0]["sessao"] == "s2"
