# FinBot

Assistente educacional para aprender conceitos sobre investimentos no Brasil. Este projeto está sendo desenvolvido passo a passo como parte das aulas.

## Etapa atual

- **Aula 1:** ambiente Python, configuração de modelos, prompts e chat pelo terminal.
- **Aula 2:** API FastAPI, frontend Streamlit e observabilidade com Langfuse e configuração para posterior deploy no Render e Streamlit Community Cloud.

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

Crie o arquivo `.env` a partir de `.env.example` e coloque sua chave em `GROQ_API_KEY` (ou configure o provedor escolhido em `LLM_PROVEDOR`). **Nunca publique o `.env` nem cole sua chave no README.**

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

## Testes

```bash
pytest -v
```

Os testes substituem o modelo por uma implementação falsa para não consumir créditos nem depender do serviço externo. Para validar a resposta real, configure sua chave e teste `POST /chat` pelo Swagger ou pelo Streamlit.

## Publicação

A API usa o `render.yaml` para o Render; configure as variáveis de ambiente secretas diretamente na plataforma. O frontend é publicado no Streamlit Community Cloud apontando `API_URL` para o serviço do Render (em Secrets).

## Links do projeto

| O quê | Link |
|---|---|
| Repositório GitHub | [MarcosAlves90/finbot](https://github.com/MarcosAlves90/finbot) |
| Chat publicado (Streamlit Cloud) | PENDENTE — preencher depois de publicar |
| API publicada (Render) | PENDENTE — preencher depois de publicar |
| Documentação da API | PENDENTE — preencher depois de publicar |

## Segurança

Este é um projeto educacional. Na Aula 2 o histórico fica temporariamente na memória da API e é identificado apenas por `sessao`, sem autenticação. Não envie informações pessoais ou confidenciais. O `.env` e `.venv/` são locais e estão no `.gitignore`.

## Materiais das aulas

A pasta `aulas/` é uma cópia integral e inalterada da pasta correspondente no ZIP original fornecido da professora, incluindo as imagens. O arquivo fornecido contém as aulas 1, 2 e 3; não contém os documentos das aulas 4 a 7.
