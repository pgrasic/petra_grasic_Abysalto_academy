from fastapi import FastAPI

app = FastAPI() #ovo je nova web aplikacija

@app.get("/")
async def root():
    return {"message": "Dobrodošli u TicketHub!"} #json