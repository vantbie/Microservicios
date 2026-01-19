from fastapi import FastAPI
from app.routers import products
from app.database.database import engine, Base

app = FastAPI(title="Products Service")

Base.metadata.create_all(bind= engine)

app.include_router(products.router)

@app.get("/")
def root():
    return {"message": "products server running"}