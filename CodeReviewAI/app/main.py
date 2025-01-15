from fastapi import FastAPI
from pydantic import BaseModel
from github import fetch_all_file_contents
from chat_gpt_analyze import analyze_code
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import redis.asyncio as redis
import hashlib
import json
import os


REDIS_URL = os.getenv("REDIS_URL")

class Item(BaseModel):
    assignment_description: str  
    github_repo_url: str  # тут можна додати більш жорстокішу типизацію за допомогою регулярних виразів
    candidate_level: str  # тут також



@asynccontextmanager
async def lifespan(app: FastAPI):

    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    app.state.redis = redis_client
    yield

    await redis_client.close()

app = FastAPI(lifespan=lifespan)

def generate_cache_key(url: str):
    return f"github_repo:{hashlib.sha256(url.encode()).hexdigest()}"

def generate_cache_key(url: str):
    return f"github_repo:{hashlib.sha256(url.encode()).hexdigest()}"

@app.post("/review", response_class=HTMLResponse)
async def review(item: Item):
    redis_client = app.state.redis
    cache_key = generate_cache_key(item.github_repo_url)


    cached_data = await redis_client.get(cache_key)
    if cached_data:
        found_files = json.loads(cached_data)
    else:
        found_files = await fetch_all_file_contents(item.github_repo_url)
        
        for key in found_files.keys():
            if isinstance(found_files[key], bytes):
                found_files[key] = found_files[key].decode('utf-8')

        await redis_client.set(cache_key, json.dumps(found_files), ex=3600)  

    file_names = "\n".join(found_files.keys())
    found_files_output = f"Files found in the repository:\n{file_names}"

    
    result = await analyze_code(
        item.assignment_description,
        found_files,
        item.candidate_level
    )
    return f"{found_files_output}\n{result}"
