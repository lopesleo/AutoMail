import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from mangum import Mangum

# Adicionar o diretório atual ao path do Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

# Imports locais
from models.response import EmailAnalysisRequest, EmailAnalysisResponse
from services.email_service import analyze_email_content

app = FastAPI(title="AutoU Email Analysis API")

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

origins = [
    FRONTEND_URL,
    "https://vercel.app", 
    "https://*.vercel.app",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Rotas diretamente no main.py
@app.get("/")
async def root():
    return {"message": "AutoU Email Analysis API is running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "email-analysis"}



@app.post("/api/email/analyze", response_model=EmailAnalysisResponse)
async def analyze_email(request: EmailAnalysisRequest):
    """
    Analisa o conteúdo de um email e retorna categoria, razão e resposta sugerida.
    """
    try:
        if not request.content or not request.content.strip():
            raise HTTPException(status_code=400, detail="Conteúdo do email não pode estar vazio")
        
        result = analyze_email_content(request.content)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

handler = Mangum(app)