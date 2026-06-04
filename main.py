from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
import psycopg
from psycopg_pool import ConnectionPool

from database import CONNECTION_STRING_LOCAL_POSTGRES
from utils.check_version import check_version_of_settings
from utils.get_all_settings import all_settings_to_machine

pools = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    pools["postgres"] = ConnectionPool(
        conninfo=CONNECTION_STRING_LOCAL_POSTGRES,
        min_size=2,
        max_size=10,
        open=True
    )
    yield
    pools["postgres"].close()

app = FastAPI(lifespan=lifespan)

def get_db():
    with pools["postgres"].connection() as conn:
        yield conn


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/collector/get-version/')
def get_version(comp_name: str, conn: psycopg.Connection = Depends(get_db)):
    with conn.cursor() as cur:
        result = check_version_of_settings(cur, comp_name)
        final = result[0]
    
    return final

@app.get('/collector/get-settings/')
def get_version(comp_name: str, conn: psycopg.Connection = Depends(get_db)):
    with conn.cursor() as cur:
        result = all_settings_to_machine(cur, comp_name)
    
    return result