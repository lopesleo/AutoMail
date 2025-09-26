# models/email_models.py
from pydantic import BaseModel

class EmailAnalysisRequest(BaseModel):
    """Modelo para o corpo da requisição que chega na API."""
    content: str

class EmailAnalysisResponse(BaseModel):
    """Modelo para a resposta que nossa API envia de volta."""
    category: str
    reason: str
    response: str