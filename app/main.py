
from fastapi import FastAPI
from app.database import engine, Base

# ایمپورت روترها از پوشه اختصاصی routers
from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_router
from app.routers.book_router import router as book_router
from app.routers.order_router import router as order_router



from fastapi import FastAPI
from fastapi_swagger import patch_fastapi


app = FastAPI(docs_url=None,swagger_ui_oauth2_redirect_url=None,    
    title="Bookshelf Online API",
    description="سیستم مدیریت فروشگاه کتاب به همراه تایید دو مرحله‌ای ",
    version="1.0.0")

patch_fastapi(app,docs_url="/swagger")



# ساخت خودکار جداول بر اساس مدل‌هایی که در دیتابیس ثبت شده‌اند
Base.metadata.create_all(bind=engine)


# ثبت کردن روترها در برنامه
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(book_router)
app.include_router(order_router)

@app.get("/")
def read_root():
    return {"message": "پروژه با موفقیت اجرا شد!"}