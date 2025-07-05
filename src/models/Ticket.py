from pydantic import BaseModel
from enum import Enum

class TicketStatus(str, Enum):
    open = "open"
    closed = "closed"

class TicketPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Ticket(BaseModel):
    id: int
    title: str
    status: TicketStatus
    priority: TicketPriority
    assignee: str 

def transform_ticket(todo: dict, user: dict) -> Ticket:
    priority_map = {0: "low", 1: "medium", 2: "high"}
    return Ticket(
        id=todo["id"],
        title=todo["todo"],
        status="closed" if todo["completed"] else "open",
        priority=priority_map[todo["id"] % 3],
        assignee=user["username"]
    )
