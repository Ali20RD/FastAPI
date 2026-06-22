from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, BaseModel
from app.controllers import auth_controller, user_controller, book_controller, order_controller


BaseModel.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bookstore API",
    description="Bookshelf Management System with RBAC and OTP Authentication",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ثبت روترها
app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(book_controller.router)
app.include_router(order_controller.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Bookshelf API",
        "docs": "/docs",
        "redoc": "/redoc",
        "roles": ["admin", "author", "user"]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Bookshelf-api"}