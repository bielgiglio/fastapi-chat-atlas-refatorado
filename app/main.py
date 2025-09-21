# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .routes import messages

app = FastAPI(title="FastAPI Chat Refatorado")

# Adiciona middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas da API
app.include_router(messages.router)

# Monta o diretório de arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", include_in_schema=False)
async def index():
    """Serve o arquivo HTML principal do chat."""
    return FileResponse("app/static/index.html")