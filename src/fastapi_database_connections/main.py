from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
import psycopg_pool
import psycopg

conn_string = "postgres://postgres@localhost"

pool = psycopg_pool.AsyncConnectionPool(conn_string, open=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await pool.open()
    yield
    await pool.close()

app = FastAPI(lifespan=lifespan)

async def get_conn():
    async with pool.connection() as conn:
	    yield conn

@app.get("/visit/")
async def add_visit(conn = Depends(get_conn)):

    async with conn.cursor() as cursor:
        # Run our queries
        await cursor.execute("insert into visits(timestamp) values (now())")
        
    return {"message": "Visit logged"}
