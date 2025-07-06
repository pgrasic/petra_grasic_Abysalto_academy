import logging
from fastapi import FastAPI, HTTPException, Query, Request
import httpx
from models.LoginRequest import LoginRequest
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from services.TicketService import get_tickets, get_ticket, get_tickets_filter, get_tickets_search, stats

api=FastAPI(debug=True)
limiter = Limiter(key_func=get_remote_address)

api.state.limiter = limiter
api.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


logger = logging.getLogger(__name__)
logging.basicConfig(filename='myapi.log', level=logging.INFO)
logger.info('Started')

@api.get("/tickets")
@limiter.limit("5/minute")
async def read_tickets(
    request:Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    headers = request.headers

    return await get_tickets(skip, limit, headers["Authorization"])

@api.get("/ticket/{id}")
@limiter.limit("5/minute")
async def read_ticket(
   id:int,
   request:Request

):

    headers = request.headers
    return await get_ticket(id, headers["Authorization"])

@api.get("/tickets/{status}/{priority}")
@limiter.limit("5/minute")
async def read_ticket_filter(
   status:str,
   priority:str,
   request:Request
):
    headers = request.headers
    return await get_tickets_filter(status, priority, headers["Authorization"])

@api.get("/tickets/{naziv}/")
@limiter.limit("5/minute")
async def read_ticket_search(
   naziv:str,
    request:Request

):
    headers = request.headers

    return await get_tickets_search(naziv, headers["Authorization"])

@api.get("/stats")
@limiter.limit("5/minute")
async def read_stats(
    request:Request

):
    headers = request.headers

    return await stats(headers["Authorization"])

@api.post("/login")
async def login(data: LoginRequest):
    async with httpx.AsyncClient() as client:
        resp = await client.post("https://dummyjson.com/auth/login", json=data.dict())

        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user = resp.json()
    return {
        "access_token": user["accessToken"],
        "token_type": "bearer"
    }