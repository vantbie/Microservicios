from fastapi import FastAPI
from app.routers import orders
from app.database.database import engine, Base

app = FastAPI(title="Order Service")

Base.metadata.create_all(bind= engine)

app.include_router(orders.router)

@app.get("/")
def root():
    return {"message": "Order server running"}