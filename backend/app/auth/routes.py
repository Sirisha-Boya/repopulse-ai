"""
Authentication routes for GitHub OAuth and token management
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
import logging

from app.database import get_db
from app.models import User
from app.config import settings
from app.auth.utils import create_access_token, create_refresh_token, verify_token, decrypt_token, encrypt_token
from app.auth.dependencies import get_current_user
from app.github.service import get_github_service, GitHubService
from app import schemas

router = APIRouter(prefix="/api/auth", tags=["auth"])
logger = logging.getLogger(__name__)


@router.get("/github/login")
async def github_login():
    """Initiate GitHub OAuth flow"""
    github_service = get_github_service()
    state = str(uuid4())
    oauth_url = github_service.get_oauth_url(state)
    
    return {
        "oauth_url": oauth_url,
        "state": state
    }


@router.post("/github/callback")
async def github_callback(
    code: str = None,
    request_data: dict = None,
    db: Session = Depends(get_db),
    github_service: GitHubService = Depends(get_github_service)
):
    """Handle GitHub OAuth callback"""
    
    # Extract code from request
    auth_code = code
    if not auth_code and request_data:
        auth_code = request_data.get("code")
    
    if not auth_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization code not provided"
        )
    
    # Exchange code for access token
    token_response = await github_service.exchange_code_for_token(auth_code)
    if not token_response or "access_token" not in token_response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to exchange code for token"
        )
    
    github_access_token = token_response["access_token"]
    
    # Get GitHub user info
    github_user = await github_service.get_user(github_access_token)
    if not github_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to fetch GitHub user"
        )
    
    # Check if user exists
    user = db.query(User).filter(User.github_id == github_user["id"]).first()
    
    if not user:
        # Create new user
        user = User(
            github_id=github_user["id"],
            github_username=github_user["login"],
            email=github_user.get("email"),
            avatar_url=github_user.get("avatar_url"),
            github_token=encrypt_token(github_access_token),
            is_admin=False
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"New user created: {user.github_username}")
    else:
        # Update existing user
        user.github_token = encrypt_token(github_access_token)
        user.last_login = datetime.utcnow()
        db.commit()
        db.refresh(user)
    
    # Generate JWT tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": schemas.UserResponse.from_orm(user)
    }


@router.post("/refresh")
async def refresh_token(
    refresh_token_data: dict,
    db: Session = Depends(get_db)
):
    """Refresh JWT access token"""
    
    token = refresh_token_data.get("refresh_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token required"
        )
    
    payload = verify_token(token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Generate new access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.get("/me", response_model=schemas.UserResponse)
async def get_authenticated_user(
    current_user: User = Depends(get_current_user)
):
    """Get current authenticated user"""
    return schemas.UserResponse.from_orm(current_user)


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_github_service)
):
    """Logout user"""
    # In practice, this would invalidate tokens in a token blacklist
    return {"message": "Successfully logged out"}
