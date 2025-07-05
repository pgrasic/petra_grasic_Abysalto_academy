from typing import Any
import httpx
from models.Ticket import Ticket, transform_ticket


async def get_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://dummyjson.com/users")
        response.raise_for_status()

        users = response.json().get("users", [])
        user = next((u for u in users if u["id"] == user_id), None)
        
        if not user:
            return dict()
        print(user_id)
        return user

async def get_tickets(skip: int, limit: int) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
        tickets = fetch_tickets(client)

        page = list[skip : skip + limit]
        return {
        "total": len(list),
        "items": page
    }
async def get_ticket(id: int) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://dummyjson.com/todos")
        response.raise_for_status()
        todos = response.json().get("todos", [])
        todo = next((t for t in todos if t["id"] == id), None)

        user = await get_user(todo["userId"])
        ticket = transform_ticket(todo,user)
        return {
        "tickets": ticket,
        "todo": todo
    }

async def get_tickets_filter(status:str,priority:str) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
        fetched_tickets = await fetch_tickets(client)
        status_filtered_tickets = [t for t in fetched_tickets if t.status == status]
        tickets = [t for t in status_filtered_tickets if t.priority == priority]
        return {
        "tickets": tickets,
    }
async def fetch_tickets(client:httpx.AsyncClient):
    response = await client.get("https://dummyjson.com/todos")
    response.raise_for_status()
    todos = response.json().get("todos", [])
    list=[]
    for todo in todos:
        user = await get_user(todo["userId"])
        ticket = transform_ticket(todo,user)
        list.append(ticket)
    return list

async def get_tickets_search(naziv:str) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
        fetched_tickets = await fetch_tickets(client)
        searched_tickets = [t for t in fetched_tickets if naziv.lower() in t.title.lower()]
        return {
        "tickets": searched_tickets,
    }