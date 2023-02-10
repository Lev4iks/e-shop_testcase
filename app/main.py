import asyncio

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.routing import APIRouter

from app.database import init_models, get_db_session
from app.routers import customer_router, product_router

app = FastAPI(title="e-shop")
main_api_router = APIRouter(dependencies=[Depends(get_db_session)])
main_api_router.include_router(customer_router, prefix="/customers", tags=["customers"])
main_api_router.include_router(product_router, prefix="/products", tags=["products"])
app.include_router(main_api_router, prefix="/api", tags=["api"])


def main():
    asyncio.get_event_loop().run_until_complete(init_models())
    asyncio.gather()
    uvicorn.run('app.main:app', host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
