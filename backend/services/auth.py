"""
用户认证服务模块
"""
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from models.user import User
from core.security import hash_password, verify_password, create_access_token, decode_access_token
from core.database import get_db
from schemas.user import UserCreate, Token

# OAuth2 密码流
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def register_user(db: Session, user_data: UserCreate) -> User:
    """
    注册新用户
    
    Args:
        db: 数据库会话
        user_data: 用户注册数据
        
    Returns:
        创建的用户对象
        
    Raises:
        HTTPException: 用户名已存在
    """
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 创建新用户
    hashed_pwd = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        hashed_password=hashed_pwd,
        role="user",
        is_banned=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    验证用户凭据
    
    Args:
        db: 数据库会话
        username: 用户名
        password: 密码
        
    Returns:
        用户对象，如果验证失败返回 None
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user


def login_user(db: Session, username: str, password: str) -> Token:
    """
    用户登录
    
    Args:
        db: 数据库会话
        username: 用户名
        password: 密码
        
    Returns:
        JWT Token
        
    Raises:
        HTTPException: 认证失败或用户被封禁
    """
    user = authenticate_user(db, username, password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if user.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="该账户已被封禁"
        )
    
    # 创建 access token
    access_token = create_access_token(data={"sub": user.username})
    
    return Token(access_token=access_token, token_type="bearer")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    获取当前登录用户
    
    Args:
        token: JWT token
        db: 数据库会话
        
    Returns:
        当前用户对象
        
    Raises:
        HTTPException: token 无效或用户不存在
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 解码 token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    # 查询用户
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    
    if user.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="该账户已被封禁"
        )
    
    return user


def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    获取当前管理员用户
    
    Args:
        current_user: 当前用户
        
    Returns:
        当前管理员用户对象
        
    Raises:
        HTTPException: 用户不是管理员
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    
    return current_user

