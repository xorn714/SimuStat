# pyrefly: ignore [missing-import]
# pyright: ignore
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
# pyright: ignore
from fastapi.middleware.cors import CORSMiddleware
from app.adapter.api.v1.router import api_router

app = FastAPI(
    title="SimuStat API",
    description="API de backend para generación y validación de números pseudoaleatorios",
    version="1.0.0"
)

# Configuración de CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar el enrutador central
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a SimuStat API! Visita /docs para la documentación interactiva."}
