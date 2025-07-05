from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.user import user_router
from router.login import login_router
from router.notif import notif_router
from router.friends import fr_router
from router.images import image_router

app = FastAPI()

# CORS настройки - ВАЖНО: добавить ДО всех роутеров
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080", 
        "http://26.165.120.232:3000",
        "http://127.0.0.1:8080",
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",
        "26.165.120.232:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods"
    ],
)

# Добавляете ваши роутеры ПОСЛЕ CORS middleware
app.include_router(user_router, tags=['User'])
app.include_router(notif_router, tags=["Notif"])
app.include_router(fr_router, tags=["Friends"])
app.include_router(image_router, tags=["Images"])
app.include_router(login_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)