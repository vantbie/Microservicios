from fastapi import FastAPI
from app.routers import users, orders, products, auth

app = FastAPI(title="API gateway")

app.include_router(users.router)
app.include_router(orders.router)
app.include_router(products.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Api Gateway server running"}

