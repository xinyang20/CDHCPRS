"""
用户认证路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.user import UserCreate, UserResponse, Token, UserUpdate
from services.auth import register_user, login_user, get_current_user
from core.security import hash_password

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    用户注册
    
    Args:
        user_data: 用户注册数据
        db: 数据库会话
        
    Returns:
        创建的用户信息
    """
    user = register_user(db, user_data)
    return user


@router.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    用户登录
    
    Args:
        form_data: OAuth2 表单数据（包含 username 和 password）
        db: 数据库会话
        
    Returns:
        JWT Token
    """
    token = login_user(db, form_data.username, form_data.password)
    return token


@router.get("/users/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    """
    获取当前用户信息
    
    Args:
        current_user: 当前登录用户
        
    Returns:
        当前用户信息
    """
    return current_user


@router.put("/users/me/password", response_model=UserResponse)
def update_password(
    password_data: UserUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    修改当前用户密码
    
    Args:
        password_data: 包含新密码的数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        更新后的用户信息
    """
    if not password_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="密码不能为空"
        )
    
    # 更新密码
    current_user.hashed_password = hash_password(password_data.password)
    db.commit()
    db.refresh(current_user)
    
    return current_user

