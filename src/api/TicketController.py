from fastapi import FastAPI, Query
from services.TicketService import get_tickets, get_ticket, get_tickets_filter, get_tickets_search

api=FastAPI(debug=True)


@api.get("/tickets")
async def read_tickets(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return await get_tickets(skip, limit)

@api.get("/ticket/{id}")
async def read_ticket(
   id:int
):
    return await get_ticket(id)

@api.get("/tickets/{status}/{priority}")
async def read_ticket_filter(
   status:str,
   priority:str
):
    return await get_tickets_filter(status, priority)

@api.get("/tickets/{naziv}/")
async def read_ticket_search(
   naziv:str,
):
    return await get_tickets_search(naziv)