# PocketSmart AI — Your Smart Budget & Recommendation Assistant

A complete FastAPI + Jinja2 + SQLite + Gemini project based on the supplied PocketSmart AI documentation.

## Features
- Home Interior Budget Planner
- Party Budget Planner
- Jewelry Budget Planner
- Optional jewelry outfit-image analysis
- Registration / login / logout
- JWT authentication via HTTP-only cookie
- Recommendation history
- Session info and session data APIs
- Recommendation details API
- Gemini AI integration with configurable model
- Fallback recommendation engine when Gemini is unavailable
- Responsive frontend
- Swagger API docs

## Setup (Windows / VS Code)
1. Install Python 3.11+.
2. Open this folder in VS Code.
3. Open Terminal > New Terminal.
4. Run:
   `python -m venv .venv`
5. Activate:
   `.venv\\Scripts\\activate`
6. Install dependencies:
   `pip install -r requirements.txt`
7. Copy `.env.example` to `.env` and add your Gemini API key if available.
8. Run:
   `uvicorn app.main:app --reload`
9. Open http://127.0.0.1:8000
10. API docs: http://127.0.0.1:8000/docs

## Run without Gemini
Leave `GEMINI_API_KEY=` empty. The built-in fallback engine keeps Home, Party and Jewelry flows testable.

## Demo data
Home: budget 50000, rooms `Living Room, Bedroom`, style `Modern`, city `Coimbatore`.
Party: budget 30000, guests `50`, event `Birthday`, venue `Function Hall`, city `Coimbatore`.
Jewelry: budget 10000, occasion `Wedding`, style `Elegant`.

## Main endpoints
Authentication: `/api/auth/register`, `/api/auth/login`, `/api/auth/logout`, `/api/auth/me`
Session: `/api/session-info`, `/api/session-data`
Planners: `/api/planners/home`, `/api/planners/party`, `/api/planners/jewelry`
History: `/api/history`, `/api/history/{history_id}`, `/api/history/{history_id}` DELETE
Details: `/api/recommendations-details/{history_id}`
System: `/health`, `/startup`

## Marketplace behavior
The source document names Amazon, Flipkart, IKEA, Swiggy, Zomato and OYO. This implementation uses safe search links and estimated prices unless official APIs are connected later; it does not claim live inventory or live pricing.

## Checks
`python -m compileall app`
`python -m pytest`
