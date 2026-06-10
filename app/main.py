
from fastapi import FastAPI
from app.database import engine, Base

# Import routers from the dedicated routers folder
from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_router
from app.routers.book_router import router as book_router
from app.routers.order_router import router as order_router



from fastapi import FastAPI
from fastapi_swagger import patch_fastapi


app = FastAPI(docs_url=None,swagger_ui_oauth2_redirect_url=None,    
    title="Bookshelf Online API",
    description="**Bookstore management system with authentication**",
    version="1.0.0")

patch_fastapi(app,docs_url="/swagger")



# Automatic generation of tables based on models registered in the database
Base.metadata.create_all(bind=engine)


# Registering routers in the program
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(book_router)
app.include_router(order_router)

@app.get("/")
def read_root():
    return {"message": "The project was successfully implemented!"}