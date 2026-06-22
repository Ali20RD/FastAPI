from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.order_service import OrderService
from app.services.permission_service import PermissionService
from app.views.order_schemas import (
    OrderCreate, OrderUpdate, OrderResponse, OrderDetailResponse, OrderItemResponse
)
from app.dependencies.auth_deps import get_current_user, require_permission
from app.models.user_model import User
from app.models.enums import OrderStatus

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """دریافت سفارشات بر اساس دسترسی کاربر"""
    order_service = OrderService(db)
    orders = order_service.get_visible_orders(current_user)
    return orders

@router.get("/{order_id}", response_model=OrderDetailResponse)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """دریافت یک سفارش خاص"""
    order_service = OrderService(db)
    permission_service = PermissionService(db)
    
    # بررسی دسترسی
    can_view, message = permission_service.can_view_order(current_user, order_id)
    if not can_view:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )
    
    order = order_service.get_order_by_id(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    items = order_service.get_order_items(order_id)
    return OrderDetailResponse.from_order(order, items)

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(require_permission("order:create")),
    db: Session = Depends(get_db)
):
    """ایجاد سفارش جدید (خرید کتاب)"""
    order_service = OrderService(db)
    
    # تبدیل داده‌ها
    books = [{'book_id': item.book_id, 'quantity': item.quantity} 
             for item in order_data.books]
    
    try:
        order = order_service.create_order(
            user_id=current_user.id,
            user_email=current_user.email,
            books=books,
            shipping_address=order_data.shipping_address
        )
        return order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    status_data: OrderUpdate,
    current_user: User = Depends(require_permission("order:update")),
    db: Session = Depends(get_db)
):
    """بروزرسانی وضعیت سفارش (فقط ادمین)"""
    order_service = OrderService(db)
    
    order = order_service.update_order_status(order_id, status_data.status)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order

@router.post("/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """لغو سفارش (کاربر خودش یا ادمین)"""
    order_service = OrderService(db)
    permission_service = PermissionService(db)
    
    # بررسی دسترسی
    can_view, message = permission_service.can_view_order(current_user, order_id)
    if not can_view:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )
    
    try:
        order = order_service.cancel_order(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        return order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{order_id}/items", response_model=List[OrderItemResponse])
async def get_order_items(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """دریافت آیتم‌های یک سفارش"""
    order_service = OrderService(db)
    permission_service = PermissionService(db)
    
    # بررسی دسترسی
    can_view, message = permission_service.can_view_order(current_user, order_id)
    if not can_view:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )
    
    items = order_service.get_order_items(order_id)
    return items