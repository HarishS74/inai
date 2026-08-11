from fastapi import APIRouter
from app.database import supabase

router = APIRouter(prefix="/company", tags=["Company"])


@router.get("/")
def get_companies():
    response = supabase.table("companies").select("*").execute()
    return response.data


@router.post("/")
def add_company():
    data = {
        "company_name": "Demo Insurance",
        "company_code": "DEMO",
        "website": "https://demo.com"
    }

    response = supabase.table("companies").insert(data).execute()
    return response.data