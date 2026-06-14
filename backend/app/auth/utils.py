"""
JWT and authentication utilities
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.using(schemes=["bcrypt"]).verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Get bcrypt hash of password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def encrypt_token(token: str) -> str:
    """Encrypt sensitive token (like GitHub token)"""
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    import base64
    
    cipher = AES.new(settings.SECRET_KEY.encode()[:32].ljust(32, b'\0'), AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(token.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()


def decrypt_token(encrypted_token: str) -> str:
    """Decrypt sensitive token"""
    from Crypto.Cipher import AES
    import base64
    
    data = base64.b64decode(encrypted_token)
    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]
    
    cipher = AES.new(settings.SECRET_KEY.encode()[:32].ljust(32, b'\0'), AES.MODE_EAX, nonce=nonce)
    token = cipher.decrypt_and_verify(ciphertext, tag)
    return token.decode()
