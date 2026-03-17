import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

app = FastAPI(title="Demo Backend", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://demo:demo@postgres.demo-apps.svc.cluster.local:5432/demo",
)


def get_greeting_from_db() -> str:
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS greetings (id SERIAL PRIMARY KEY, message TEXT NOT NULL)"
            )
            cur.execute("SELECT message FROM greetings ORDER BY id LIMIT 1")
            row = cur.fetchone()
            if row is None:
                cur.execute(
                    "INSERT INTO greetings (message) VALUES (%s) RETURNING message",
                    ("Hello from the demo backend!",),
                )
                row = cur.fetchone()
            conn.commit()
            return row[0]
    finally:
        conn.close()


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/api/greeting")
def greeting():
    message = get_greeting_from_db()
    return {"message": message}
