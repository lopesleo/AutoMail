import PyPDF2
import io
from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from models.response import EmailAnalysisResponse
from services import email_service

router = APIRouter(
    prefix="/api/email",  
    tags=["Email Analysis"] 
)

@router.post("/analyze", response_model=EmailAnalysisResponse)
async def analyze_unified_endpoint(
    content: Optional[str] = Form(None), 
    file: Optional[UploadFile] = File(None)
):
    """
    Rota unificada para analisar um email.

    Pode receber o conteúdo de duas formas (DÊ PREFERÊNCIA AO ARQUIVO):
    1. Um arquivo (.txt ou .pdf) enviado no campo 'file'.
    2. Um texto simples enviado no campo 'content'.

    Se ambos forem enviados, o arquivo será processado.
    """
    email_text = ""

    if file:
        if file.filename.endswith('.txt'):
            contents_bytes = await file.read()
            email_text = contents_bytes.decode('utf-8')
        elif file.filename.endswith('.pdf'):
            try:
                pdf_bytes = await file.read()
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
                text_parts = [page.extract_text() for page in pdf_reader.pages]
                email_text = " ".join(filter(None, text_parts)) 
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Erro ao ler o arquivo PDF: {e}")
        else:
            raise HTTPException(status_code=400, detail="Formato de arquivo não suportado. Use .txt ou .pdf.")
    
    elif content:
        email_text = content
    
    else:
        raise HTTPException(status_code=400, detail="Nenhum conteúdo de email ou arquivo foi enviado.")

    if not email_text or not email_text.strip():
        raise HTTPException(status_code=400, detail="O conteúdo do email está vazio.")

    try:
        return email_service.analyze_email_content(email_text)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")