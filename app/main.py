from fastapi import FastAPI
from app.routers import eleccion

app = FastAPI()

app.include_router(eleccion.router)

@app.get("/")
def root():
    return {"message": "Welcome to this API!!"}