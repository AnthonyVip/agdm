from fastapi import FastAPI
from app.v1.router.user_route import router as user_router
from app.v1.router.transaction_route import router as transaction_router

app = FastAPI()
app.include_router(user_router)
app.include_router(transaction_router)
