# FinBot — Aulas 1 e 2

Projeto educacional de chatbot para **explicar conceitos de investimentos no Brasil**. Não realiza recomendações de compra ou venda. Implementação desenvolvida para acompanhar a proposta das aulas 1 e 2 da disciplina.

## Requisitos

Python 3.12 ou superior, Git e uma chave de API da Groq, Gemini ou Mistral.

## Configuração inicial

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
```

No Windows PowerShell, use `py -3.12 -m venv .venv`, `.venv\Scripts\Activate.ps1` e `Copy-Item .env.example .env`.
Edite o `.env` com a chave de API correspondente ao provedor selecionado.

**Nunca publique `.env`, credenciais nem `.venv`.**

A documentação será complementada com o chat em terminal, a API e o frontend.

## Aula 1 — chat no terminal

```bash
python -m scripts.chat_terminal
```

Digite `sair` para encerrar. O histórico existe apenas enquanto o processo permanece aberto.

## Testes

```bash
pytest -q
```

Os testes automatizados são independentes das chamadas pagas ou gratuitas ao provedor.
Veja também `docs/experimentos-aula-1.md` para os experimentos manuais previstos.
