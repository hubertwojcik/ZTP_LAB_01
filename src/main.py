from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import api_router

app = FastAPI(
    title="ZTP Lab 01",
    description="Zadanie 1",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "FastAPI is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}

