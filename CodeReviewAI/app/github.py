import base64
import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()

GiTHUB_TOKEN = os.getenv("GITHUB_API_KEY")
GITHUB_API_URL = "https://api.github.com"

async def fetch_all_file_contents(url: str):
    if "github.com" not in url:
        raise ValueError("URL повинен бути у форматі GitHub.")
    
    parts = url.rstrip('/').split('/')
    if len(parts) < 5:
        raise ValueError("Неправильний формат url адреси. Очікуваний формат: https://github.com/owner/repo")
    
    owner = parts[3]  
    repo = parts[4]   
    headers = {
        "Authorization": f"Bearer {GiTHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    url_recur = f"{GITHUB_API_URL}/repos/{owner}/{repo}/git/trees/main?recursive=1"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url_recur) as resp:
            resp.raise_for_status()
            tree = (await resp.json())["tree"] 

        file_of_content = {}

        for item in tree:
            if item["type"] == "blob":
                blob_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/git/blobs/{item['sha']}"
                async with session.get(blob_url) as blob_resp:
                    blob_resp.raise_for_status()
                    blob_data = await blob_resp.json()

                content = base64.b64decode(blob_data["content"])
                file_of_content[item["path"]] = content
    return file_of_content
