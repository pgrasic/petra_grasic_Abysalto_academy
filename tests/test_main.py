import pytest
from models.Ticket import Ticket
from services.TicketService import get_tickets, get_user, get_ticket, get_tickets_filter,get_tickets_search

AUTH = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJlbWlseXMiLCJlbWFpbCI6ImVtaWx5LmpvaG5zb25AeC5kdW1teWpzb24uY29tIiwiZmlyc3ROYW1lIjoiRW1pbHkiLCJsYXN0TmFtZSI6IkpvaG5zb24iLCJnZW5kZXIiOiJmZW1hbGUiLCJpbWFnZSI6Imh0dHBzOi8vZHVtbXlqc29uLmNvbS9pY29uL2VtaWx5cy8xMjgiLCJpYXQiOjE3NTE4MDQ3NDcsImV4cCI6MTc1MTgwODM0N30.1ThWMCHQGR_SZ5P6_HkqPDJJtwmcWLxyp3jihI8Zi5c"  

@pytest.mark.asyncio
async def test_get_tickets_list():
    response = await get_tickets(0,5,AUTH)
    assert len(response) > 0
    assert len(response) <=5

@pytest.mark.asyncio
async def test_get_tickets_search():
    response = await get_tickets_search("Movie", AUTH)
    assert len(response) > 0

@pytest.mark.asyncio
async def test_get_tickets_filter():
    response = await get_tickets_filter("closed", "low", AUTH)
    assert len(response) > 0
@pytest.mark.asyncio
async def test_user_list():
    response = await get_user(1) 
    assert isinstance(response, dict)
    assert response["id"] == 1
    assert "firstName" in response

@pytest.mark.asyncio
async def test_get_user_nonexistent():
    response = await get_user(99999)
    assert response == {}
@pytest.mark.asyncio
async def test_get_ticket_existing():
    response = await get_ticket(1, AUTH) 
    print(response)
    assert isinstance(response, dict)
    assert "tickets" in response
    assert "todo" in response
    assert response["todo"]["id"] == 1
    assert isinstance(response["tickets"], Ticket)

@pytest.mark.asyncio
async def test_get_ticket_nonexistent():
    with pytest.raises(Exception): 
        await get_ticket(99999, AUTH)