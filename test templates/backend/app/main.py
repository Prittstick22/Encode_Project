import os
HELIUS_KEY = os.getenv("HELIUS_API_KEY")
HELIUS_RPC = os.getenv("HELIUS_RPC_URL")
from fastapi import FastAPI
app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}
