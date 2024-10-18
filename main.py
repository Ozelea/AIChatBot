from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.api import routers  # Importing your router

app = FastAPI()

# Configure CORS
origins = ["*"]  # Allow all origins (adjust this for better security in production)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # Which domains are allowed to access the API
    allow_credentials=True,        # Whether cookies or authentication headers are allowed
    allow_methods=["*"],           # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],           # Allow all headers
)

# Include your routers
app.include_router(routers)

# Optionally, add any other routes or middleware below