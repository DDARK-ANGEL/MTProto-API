from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import httpx

app = FastAPI()

API_URL = "https://mtpro.xyz/api/?type=mtproto"

@app.get("/{region}")
async def get_proxy(region: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch proxy list")
        
        proxies = response.json()
        for proxy in proxies:
            if proxy.get("country").lower() == region.lower():
                url = f"https://t.me/proxy?server={proxy['host']}&port={proxy['port']}&secret={proxy['secret']}"
                return RedirectResponse(url)
        
        raise HTTPException(status_code=404, detail="No proxy found for the specified region")