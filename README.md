# TicketHub API – Abysalto AI Academy 2025

FastAPI REST API for managing tickets using public data from [DummyJSON](https://dummyjson.com/).
Developed as a technical assignment for the AI Academy 2025.

---
Testing and README formatting assisted by ChatGPT using the Canvas feature.
---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/pgrasic/petra_grasic_Abysalto_academy.git
cd petra_grasic_Abysalto_academy/src
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI server

```bash
uvicorn src.api.TicketController:api --reload
```

---

##  Features

* JWT authentication using DummyJSON login
* Paginated list of tickets
* Filtering by status and priority
* Full-text search by ticket title
* Aggregated ticket statistics:

  * Total ticket count
  * Status & priority counters
  * Closed/open ratio
  * User with most tickets
  * Relative priority frequencies
* User data joined to each ticket
*  Minimal test suite with `pytest`

---

## Authentication

Login uses the DummyJSON `/auth/login` endpoint.
On successful login, it returns an `access_token` that should be used in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

---

## API Endpoints

| Endpoint                       | Method | Description                                    |
| ------------------------------ | ------ | ---------------------------------------------- |
| `/login`                       | POST   | Authenticates the user and returns a JWT token |
| `/tickets`                     | GET    | Returns a list of tickets with pagination      |
| `/ticket/{id}`                 | GET    | Returns ticket details + raw JSON              |
| `/tickets/{status}/{priority}` | GET    | Filters tickets by status and priority         |
| `/tickets/{name}/`             | GET    | Searches tickets by name                       |
| `/stats`                       | GET    | Aggregated statistics of all tickets           |
| `/me` *(optional)*             | GET    | Authenticated route for token verification     |

---

## Ticket Statistics (`/stats`)

* Total number of tickets
* Ticket count per status
* Ticket count per priority
* Number of tickets per user
* Most common status
* User with the most tickets
* Percentage of closed tickets
* Relative frequency of each priority

---

## Running Tests

Make sure you're using the correct environment:

```bash
PYTHONPATH=src pytest -v
```

### Tests included:

* Ticket list pagination
* Ticket details
* Filters
* Search
* Aggregated statistics
* Login authentication
* Authenticated route test

---

## ⚙️ Project Structure

```
src/
├── api/              # FastAPI routes (TicketController.py)
├── models/           # Pydantic models (Ticket, LoginRequest)
├── services/         # Business logic for tickets
tests/                # Pytest-based tests
```

---

## Author

**Petra Grasic**
GitHub: [@pgrasic](https://github.com/pgrasic)
Project for: *Abysalto AI Academy 2025*
