from fastapi import FastAPI
from routers import  trading


app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return {"message": "My e-commerce app"}


app.include_router(trading.router)