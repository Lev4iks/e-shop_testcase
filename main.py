import uvicorn
from fastapi import FastAPI, Request
from fastapi.routing import APIRouter

from app.handlers import user_router
from app.helpers import cli

app = FastAPI(title="e-shop")
main_api_router = APIRouter()
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)

if __name__ == "__main__":
    # cli()
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)
