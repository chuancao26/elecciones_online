from fastapi import FastAPI
from app.routers import eleccion, lista, elector, auth

app = FastAPI()

app.include_router(eleccion.router)
app.include_router(lista.router)
app.include_router(elector.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to this API!!"}