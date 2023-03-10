import asyncio

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.routing import APIRouter

from app.config import insert_start_data
from app.database import init_models, get_db_session, init_start_data
from app.routers import customer_router, product_router, cart_router

app = FastAPI(title="e-shop")
main_api_router = APIRouter(dependencies=[Depends(get_db_session)])
main_api_router.include_router(customer_router, prefix="/customers", tags=["customers"])
main_api_router.include_router(product_router, prefix="/products", tags=["products"])
main_api_router.include_router(cart_router, prefix="/cart", tags=["cart"])
app.include_router(main_api_router, prefix="/api", tags=["api"])


def main():
    asyncio.get_event_loop().run_until_complete(init_models())
    if insert_start_data:
        asyncio.get_event_loop().run_until_complete(init_start_data())
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
