from fastapi import FastAPI
from app.routers import users
from app.database.database import engine, Base

app = FastAPI(title="Users service") #Instaciamos nuestra api

Base.metadata.create_all(bind= engine)

app.include_router(users.router)

@app.get("/") # un get para visualizar que la pagina corra
def root():
    return {"status":"users service running"}

