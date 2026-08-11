from fastapi import FastAPI

from app.api.company import router as company_router
from app.api.ai import router as ai_router
from app.api.upload import router as upload_router

app = FastAPI(title="INAI API")

app.include_router(company_router)
app.include_router(ai_router)
app.include_router(upload_router)