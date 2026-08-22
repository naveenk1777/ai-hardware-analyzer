# IoT Predictive Cloud Bridge 🚀

An asynchronous Python backend that bridges ESP32 edge hardware with cloud infrastructure. It ingests sensor telemetry in real-time, stores it in a serverless PostgreSQL database, and utilizes Google's Gemini AI to perform predictive maintenance and hardware diagnostics.

## System Architecture
* **Hardware:** ESP32 (simulated) sending HTTP POST requests.
* **API Gateway:** FastAPI running asynchronously via Uvicorn.
* **Database:** PostgreSQL (Neon) managed by SQLAlchemy 2.0 (asyncpg).
* **AI Engine:** Gemini 2.5 Flash API with strict Pydantic structured JSON outputs.

## Setup Instructions
1. Clone the repository.
2. Run `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and insert your credentials.
4. Run the server: `uvicorn main:app --reload`.

## Endpoints
* `POST /api/telemetry` (Secured via X-Hardware-Key header)
* `POST /api/diagnose/{device_id}` (Triggers AI analysis)
