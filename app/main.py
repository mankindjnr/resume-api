from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from .routers import summarysection
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(summarysection.router)

@app.get("/")
def root():
    return {"message": "mankindjnr resume to the World"}