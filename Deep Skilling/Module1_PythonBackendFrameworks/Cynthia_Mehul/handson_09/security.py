from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

# bcrypt is preferred for password hashing because it is intentionally slow
# and uses a unique salt for each password, making brute-force and rainbow
# table attacks much harder. MD5 and SHA-256 (doesnt add unique salt) are designed to be fast and are
# therefore unsuitable for securely storing passwords.


# OAuth2 Authorization Code Flow:
# The user authenticates with an authorization server, which issues an
# authorization code. The client exchanges this code for an access token.
#
# This project uses a simpler JWT login where the user sends email and
# password directly to the API, which immediately returns a JWT after
# successful authentication.


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt

