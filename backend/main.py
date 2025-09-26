from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()
from routers import email
app = FastAPI()
# Lista de origens que podem fazer requisições à sua API
origins = [
    "http://localhost:3000", # A URL do seu frontend Next.js em desenvolvimento
    # Você pode adicionar a URL de produção aqui no futuro, se necessário
    # "https://seu-site-em-producao.vercel.app", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todos os cabeçalhos
)
app.include_router(email.router)
