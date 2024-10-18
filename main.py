from fastapi import FastAPI
from routers.api import routers

app = FastAPI()
app.include_router(routers)
