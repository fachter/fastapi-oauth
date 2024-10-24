import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()
load_dotenv()
github_client_id = os.getenv("GITHUB_CLIENT_ID")
github_client_secret = os.getenv("GITHUB_CLIENT_SECRET")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/github-login")
async def github_login():
    return RedirectResponse(
        f"https://github.com/login/oauth/authorize?client_id={github_client_id}",
        status_code=302
    )

@app.get("/github-code")
async def github_code(code: str):
    params = {
        'client_id': github_client_id,
        'client_secret': github_client_secret,
        'code': code
    }
    headers = {'Accept': 'application/json'}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url="https://github.com/login/oauth/access_token",
            headers=headers,
            params=params,
        )
    response_json = response.json()
    access_token = response_json.get('access_token')
    async with httpx.AsyncClient() as client:
        headers.update({'Authorization': f'Bearer {access_token}'})
        response = await client.get('https://api.github.com/user', headers=headers)
    return (response.json())