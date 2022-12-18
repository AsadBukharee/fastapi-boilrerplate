import jwt
from fastapi_jwt_auth import AuthJWT
from passlib import pwd
from passlib.context import CryptContext
from typing import Optional
from datetime import datetime, timedelta
from core.project_settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings().SECRET_KEY, algorithm=settings().ALGORITHM)
    return encoded_jwt


def generate_password(size=9, custom=True):
    """
    minimum length returned is 9.
    "ascii_62" (the default) – all digits and ascii upper & lowercase letters.
    Provides ~5.95 entropy per character.
    "ascii_50" – subset which excludes visually similar characters (1IiLl0Oo5S8B).
    Provides ~5.64 entropy per character.
    "ascii_72" – all digits and ascii upper & lowercase letters, as well as some punctuation.
     Provides ~6.17 entropy per character.
    "hex" – Lower case hexadecimal. Providers 4 bits of entropy per character.
    """
    if custom:
        # confusing letters (1IiLl0OoS5) are excluded.
        characters = "abcdefghjkmnpqrtuvwxyzABCDEFGHJKMNPQRSTUVWXYZ2346789!@#-$%&?;*"
        return pwd.genword(length=size, entropy=52, chars=characters)
    else:
        return pwd.genword(length=size, entropy=52, charset="ascii_72")


def get_current_logged_in_user(authorize, response_body):
    current_user = None
    try:
         current_user = authorize.get_jwt_subject()
    except:
        current_user = None

    if current_user == None:
        access_token = response_body.get("access_token",None)
        if access_token:
            current_user = authorize._verified_token(access_token)['sub']

    return current_user

def auth_jwt_verifier_and_get_subject(request):
    authorize=AuthJWT(request)
    current_user_email = authorize.get_jwt_subject()
    return current_user_email