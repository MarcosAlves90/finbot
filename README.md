# FinBot

Assistente educacional para aprender conceitos sobre investimentos no Brasil e consultar dados de mercado em tempo real. Este projeto está sendo desenvolvido passo a passo como parte das aulas.

## Etapa atual

- **Aula 1:** ambiente Python, configuração de modelos, prompts e chat pelo terminal.
- **Aula 2:** API FastAPI, frontend Streamlit e observabilidade com Langfuse e configuração para posterior deploy no Render e Streamlit Community Cloud.
- **Aula 3:** memória persistente por sessão no MongoDB e prompts versionados no Langfuse.
- **Aula 4:** agente com ferramentas para consultar indicadores do Banco Central, cotações de ações, FIIs e Tesouro Direto; o token da brapi.dev é opcional.

## Requisitos

- Python 3.12
- Uma chave válida da Groq, Gemini ou Mistral

## Configurar o ambiente

Na raiz do projeto, ative o ambiente e instale as dependências:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
pip install -r requirements-dev.txt
```

Crie o arquivo `.env` a partir de `.env.example` e coloque sua chave em `GROQ_API_KEY` (ou configure o provedor escolhido em `LLM_PROVEDOR`). Para consultar ativos fora da lista gratuita da brapi.dev, preencha também `BRAPI_TOKEN` (opcional). **Nunca publique o `.env` nem cole suas chaves no README.**

## Como executar

Chat no terminal (Aula 1):

```bash
python -m scripts.chat_terminal
```

API (Aula 2):

```bash
uvicorn app.main:app --reload
```

Documentação interativa: http://127.0.0.1:8000/docs

Em outro terminal, com ambiente virtual ativo:

```bash
pip install -r frontend/requirements.txt
streamlit run frontend/streamlit_app.py
```

Interface local: http://localhost:8501

Ferramentas de mercado (Aula 4; consulta APIs reais):

```bash
python -m app.tools.mercado
```

## Testes

```bash
pytest -v
```

Os testes substituem o modelo, o MongoDB e as APIs de mercado por implementações falsas; não consomem créditos nem dependem de serviços externos. Para validar respostas reais, configure as chaves e teste `POST /chat` pelo Swagger ou pelo Streamlit.

## Publicação

A API usa o `render.yaml` para o Render; configure as variáveis de ambiente secretas diretamente na plataforma. Se usar `BRAPI_TOKEN`, cadastre-o como segredo no serviço `finbot-api`. O frontend é publicado no Streamlit Community Cloud apontando `API_URL` para o serviço do Render (em Secrets).

## Links do projeto

| O quê | Link |
|---|---|
| Repositório GitHub | [MarcosAlves90/finbot](https://github.com/MarcosAlves90/finbot) |
| Chat publicado (Streamlit Cloud) | [finbot-marcos.streamlit.app](https://finbot-marcos.streamlit.app/) |
| API publicada (Render) | [finbot-api-i96n.onrender.com](https://finbot-api-i96n.onrender.com) |
| Documentação da API (Swagger) | [Abrir documentação](https://finbot-api-i96n.onrender.com/docs) |

## Segurança

Este é um projeto educacional. A API não tem autenticação; as conversas são identificadas por `sessao` e persistidas no MongoDB. Não envie informações pessoais ou confidenciais. O `.env` e `.venv/` são locais e estão no `.gitignore`.

## Materiais das aulas

Os materiais das aulas 1–3 foram preservados como cópia integral e inalterada da pasta correspondente no ZIP original fornecido pela professora. A Aula 4 (`aulas/aula-04.md`) e suas imagens foram obtidas do repositório `profcintiapinho/chat_multiagente_inves`, no commit `4c2c2ce544b78151075cce4bb406704de4660e4f`. Não há materiais das aulas 5–7 no repositório consultado.
