from fastapi import FastAPI
from api_v1.users.views import router as users_router

app = FastAPI()
app.include_router(users_router)

@app.get("/")
async def hello():
    return {"message": "Hello, World!"}