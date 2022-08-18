from fastapi.middleware.cors import CORSMiddleware

from app import app

origins = ["10.10.120.140", "http://localhost", "http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
