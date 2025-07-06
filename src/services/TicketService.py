import logging
from typing import Any
from fastapi import HTTPException
import httpx
from models.Ticket import Ticket, transform_ticket
from collections import Counter

logger = logging.getLogger(__name__)
logging.basicConfig(filename='myapi.log', level=logging.INFO)
logger.info('API service started')

async def get_user(user_id: int):
    logger.info(f"Fetching user with ID: {user_id}")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://dummyjson.com/users")
            response.raise_for_status()
            users = response.json().get("users", [])
            user = next((u for u in users if u["id"] == user_id), None)
            if not user:
                logger.warning(f"User with ID {user_id} not found")
                return dict()
            logger.info(f"Found user: {user['firstName']} {user['lastName']}")
            return user
        except httpx.HTTPError as e:
            logger.error(f"Error fetching user: {e}")
            return dict()

async def get_tickets(skip: int, limit: int, access_token) -> dict[str, Any]:
    logger.info("Getting tickets with pagination")
    if not await check_user(access_token):
        logger.warning("Invalid credentials for ticket listing")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    async with httpx.AsyncClient() as client:
        tickets = await fetch_tickets(client)
        logger.info(f"Fetched {len(tickets)} tickets")
        page = tickets[skip : skip + limit]
        return {
            "total": len(tickets),
            "items": page
        }

async def get_ticket(id: int, access_token) -> dict[str, Any]:
    logger.info(f"Getting ticket with ID: {id}")
    if not await check_user(access_token):
        logger.warning("Invalid credentials for single ticket access")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    async with httpx.AsyncClient() as client:
        response = await client.get("https://dummyjson.com/todos")
        response.raise_for_status()
        todos = response.json().get("todos", [])
        todo = next((t for t in todos if t["id"] == id), None)

        if not todo:
            logger.warning(f"Todo with ID {id} not found")
            return {
            "tickets": "empty",
            "todo": "empty"
                    }
        user = await get_user(todo["userId"])
        ticket = transform_ticket(todo, user)
        logger.info(f"Returned ticket and todo for ID: {id}")
        return {
            "tickets": ticket,
            "todo": todo
        }

async def get_tickets_filter(status: str, priority: str, access_token) -> dict[str, Any]:
    logger.info(f"Filtering tickets with status '{status}' and priority '{priority}'")
    if not await check_user(access_token):
        logger.warning("Invalid credentials for filtering")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    async with httpx.AsyncClient() as client:
        fetched_tickets = await fetch_tickets(client)
        status_filtered_tickets = [t for t in fetched_tickets if t.status == status]
        tickets = [t for t in status_filtered_tickets if t.priority == priority]
        logger.info(f"Found {len(tickets)} tickets after filtering")
        return {
            "tickets": tickets
        }

async def fetch_tickets(client: httpx.AsyncClient):
    logger.info("Fetching all tickets")
    response = await client.get("https://dummyjson.com/todos")
    response.raise_for_status()
    todos = response.json().get("todos", [])
    result = []
    for todo in todos:
        user = await get_user(todo["userId"])
        ticket = transform_ticket(todo, user)
        result.append(ticket)
    logger.info(f"Transformed {len(result)} tickets")
    return result

async def get_tickets_search(naziv: str, access_token) -> dict[str, Any]:
    logger.info(f"Searching tickets with title containing '{naziv}'")
    if not await check_user(access_token):
        logger.warning("Invalid credentials for search")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    async with httpx.AsyncClient() as client:
        fetched_tickets = await fetch_tickets(client)
        searched_tickets = [t for t in fetched_tickets if naziv.lower() in t.title.lower()]
        logger.info(f"Found {len(searched_tickets)} matching tickets")
        return {
            "tickets": searched_tickets
        }

async def stats(access_token):
    logger.info("Generating statistics")
    if not await check_user(access_token):
        logger.warning("Invalid credentials for stats")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    async with httpx.AsyncClient() as client:
        fetched_tickets = await fetch_tickets(client)
        total = len(fetched_tickets)
        logger.info(f"Total number of tickets: {total}")

        status_counter = Counter(t.status for t in fetched_tickets)
        priority_counter = Counter(t.priority for t in fetched_tickets)
        ticket_per_user = Counter(t.asignee for t in fetched_tickets)

        most_loaded_user = max(ticket_per_user, key=ticket_per_user.get, default=None)
        max_tickets = ticket_per_user.get(most_loaded_user, 0)

        ratio_closed = round((status_counter.get("closed", 0) / total) * 100, 2)
        most_common_status = status_counter.most_common(1)[0][0] if status_counter else None
        priority_relative = {
            priority: round(count / total, 3)
            for priority, count in priority_counter.items()
        }

        logger.info("Stats generation completed")

        return {
            "total": total,
            "status_counter": dict(status_counter),
            "priority_counter": dict(priority_counter),
            "ticket_per_user": dict(ticket_per_user),
            "most_loaded_user": most_loaded_user,
            "ratio_closed": ratio_closed,
            "priority_relative": priority_relative,
            "most_common_status": most_common_status
        }

async def check_user(access_token):
    logger.info("Checking user authorization")
    async with httpx.AsyncClient() as client:
        response = await client.get("https://dummyjson.com/auth/me", headers={"Authorization": f"{access_token}"})
        if response.status_code != 200:
            logger.warning("User check failed: Unauthorized")
            return False
        logger.info("User authenticated successfully")
        return True
