import bcrypt
import jwt
from app.config import JWT_SECRET, ALGORITHM

def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain, hashed):
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_jwt(payload: dict):
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)

def decode_jwt(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
