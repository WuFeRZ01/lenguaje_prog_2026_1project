from fastapi import FastAPI
from api.routers import members

app = FastAPI()

app.include_router(members.router)

@app.get("/")
def root():
    return {"message": "API funcionando"}