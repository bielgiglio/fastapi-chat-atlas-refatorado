# FastAPI Chat (Refatorado) + MongoDB Atlas

Este é um projeto de chat em tempo real desenvolvido com FastAPI, MongoDB Atlas e WebSockets. O código foi refatorado para seguir boas práticas de organização, modularidade e manutenibilidade.

## Como Rodar o Projeto

### Pré-requisitos
- Python 3.8+
- Uma conta no MongoDB Atlas

### Passos
1.  **Clone o repositório** e navegue até a pasta do projeto.

2.  **Configure o MongoDB Atlas**:
    - Crie um cluster gratuito no [MongoDB Atlas](https://cloud.mongodb.com).
    - Em **Database Access**, crie um usuário e senha.
    - Em **Network Access**, libere seu IP (ou `0.0.0.0/0` para testes).
    - Copie a **Connection String** (use a opção "driver: Python").

3.  **Configure as variáveis de ambiente**:
    - Renomeie o arquivo `.env.example` para `.env`.
    - Cole sua Connection String do MongoDB na variável `MONGO_URL`.

4.  **Instale as dependências e rode o servidor**:

    ```bash
    # Crie e ative um ambiente virtual
    python -m venv .venv
    
    # Windows
    .venv\Scripts\activate
    
    # Linux/macOS
    source .venv/bin/activate
    
    # Instale as dependências
    pip install -r requirements.txt
    
    # Inicie o servidor
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

5.  **Acesse a aplicação**:
    - **Cliente do Chat**: [http://localhost:8000](http://localhost:8000)
    - **Documentação da API**: [http://localhost:8000/docs](http://localhost:8000/docs)

## Principais Endpoints

-   **WebSocket**: `ws://localhost:8000/ws/{room}`
-   **Histórico REST**: `GET /rooms/{room}/messages?limit=20`
-   **Enviar (REST)**: `POST /rooms/{room}/messages`