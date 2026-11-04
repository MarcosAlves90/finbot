# Aula 1 — Experimentos propostos

Estes experimentos dependem de uma chave válida de LLM e **não foram executados automaticamente** no ambiente sem credenciais.

## 1. Histórico de conversa

Execute `python -m scripts.chat_terminal`, apresente um nome fictício e pergunte depois qual foi o nome. Observe que o script reenvia o histórico a cada chamada. Reinicie o programa e repita a última pergunta para verificar que o histórico não sobrevive ao reinício.

## 2. Temperatura

Altere `temperatura` de `criar_modelo()` entre 0.0 e 0.8 e compare a variabilidade de respostas à mesma pergunta. A resposta pode mudar em ambos os casos: temperatura baixa não garante determinismo.

## 3. Uso de tokens

Faça uma pergunta breve e depois uma pergunta extensa, registrando `input_tokens` e `output_tokens` retornados pelo provedor. Compare o custo relativo em tokens.

## 4. Segurança

Verifique que `.env` não aparece em `git status` e que `.env.example` não contém chaves privadas.
