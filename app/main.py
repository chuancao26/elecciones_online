from fastapi import FastAPI
from app.routers import eleccion, lista, elector

app = FastAPI()

app.include_router(eleccion.router)
app.include_router(lista.router)
app.include_router(elector.router)

@app.get("/")
def root():
    return {"message": "Welcome to this API!!"}