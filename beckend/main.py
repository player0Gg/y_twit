from fastapi import FastAPI
from router import login, user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url="/")

app.include_router(login.login_router, tags=["Auth"])
app.include_router(user.user_router, tags=["User"])

# Разрешаем доступ фронту (например, Next.js на localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://26.165.120.232:3000"],  # можно временно поставить ["*"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Простой маршрут
@app.get("/api/hello")
def hello():
    return {"message": "Привет от FastAPI!"}

# Можно добавить другие маршруты здесь же
@app.get("/api/user")
def get_user():
    return {"username": "playerGg", "status": "active"}
