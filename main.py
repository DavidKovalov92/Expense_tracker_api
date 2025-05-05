from fastapi import FastAPI
from api_v1.users.views import router as users_router
from api_v1.expenses.views import router as expenses_router
from api_v1.demo_auth.views import router as demo_auth_router
from api_v1.demo_auth.demo_jwt_auth import router as jwt_auth_router

app = FastAPI()
app.include_router(users_router)
app.include_router(expenses_router)
app.include_router(demo_auth_router)
app.include_router(jwt_auth_router)

@app.get("/")
async def hello():
    return {"message": "Hello, World!"}