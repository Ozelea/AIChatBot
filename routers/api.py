from fastapi import APIRouter
from routers.v1 import chatbot_router
# from routers.v1 import balance_chatbot

routers=APIRouter()
routers.include_router(chatbot_router.router)
# routers.include_router(balance_chatbot.router)