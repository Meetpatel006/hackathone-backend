from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from bson import ObjectId

from app.core.security import get_current_active_user, get_admin_user
from ...models.user import User, UserUpdate, UserInDB
from ...crud.crud_user import user as crud_user

router = APIRouter()

def standard_response(success: bool, data: any = None, message: str = "", status_code: int = 200):
    return {
        "success": success,
        "data": data,
        "message": message,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@router.get("/me")
async def read_user_me(current_user: dict = Depends(get_current_active_user)):
    """
    Get current user
    """
    user = await crud_user.get(current_user["user_id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return standard_response(True, data=user, message="User profile fetched successfully")

@router.put("/me")
async def update_user_me(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Update current user
    """
    user = await crud_user.update(current_user["user_id"], user_update)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return standard_response(True, data=user, message="User profile updated successfully")

@router.delete("/me")
async def delete_user_me(
    current_user: dict = Depends(get_current_active_user)
):
    """
    Delete current user
    """
    success = await crud_user.delete(current_user["user_id"])
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return standard_response(True, message="User deleted successfully")

# Admin only endpoints
@router.get("/")
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_admin_user)
):
    """
    Retrieve users (admin only)
    """
    # In a real app, you would implement pagination
    users = []
    cursor = crud_user.collection.find().skip(skip).limit(limit)
    async for user_data in cursor:
        users.append(UserInDB(**user_data))
    return standard_response(True, data={"items": users, "skip": skip, "limit": limit}, message="Users fetched successfully")

@router.get("/{user_id}")
async def read_user(
    user_id: str,
    current_user: dict = Depends(get_admin_user)
):
    """
    Get user by ID (admin only)
    """
    user = await crud_user.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return standard_response(True, data=user, message="User fetched successfully")

@router.put("/{user_id}")
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_user: dict = Depends(get_admin_user)
):
    """
    Update user (admin only)
    """
    user = await crud_user.update(user_id, user_update)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return standard_response(True, data=user, message="User updated successfully")

@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    current_user: dict = Depends(get_admin_user)
):
    """
    Delete user (admin only)
    """
    # Prevent deleting yourself
    if user_id == current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own user account"
        )
        
    success = await crud_user.delete(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return standard_response(True, message="User deleted successfully")
