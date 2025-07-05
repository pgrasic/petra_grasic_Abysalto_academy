from fastapi import FastAPI,APIRouter, Query
from services.TicketService import get_tickets

app = FastAPI() #ovo je nova web aplikacija

router = APIRouter()
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Dobrodošli u TicketHub!"} #json
