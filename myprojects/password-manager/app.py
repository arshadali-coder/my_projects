from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import vault  # Your original logic file

app = FastAPI()

# CORS setup for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specific Netlify domain
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/vault")
async def run_vault(request: Request):
    body = await request.json()
    cmd = body.get("cmd")
    response = vault.handle_command(cmd)
    return {"response": response}
