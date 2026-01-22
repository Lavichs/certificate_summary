from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.main_router import router

app = FastAPI(docs_url="/api/docs")


app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

app.include_router(router)