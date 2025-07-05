import httpx
from fastapi import HTTPException
from Ticket import transform_ticket

async def get_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://dummyjson.com/users")
        response.raise_for_status()

        users = response.json().get("users", [])
        user = next((u for u in users if u["id"] == user_id), None)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

async def get_tickets():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://dummyjson.com/todos")
        response.raise_for_status()
        todos = response.json().get("todos", [])
        list=[]
        for todo in todos:
            user = await get_user(todo["userId"])
            ticket = transform_ticket(todo,user)
            list.append(ticket)
        return list
