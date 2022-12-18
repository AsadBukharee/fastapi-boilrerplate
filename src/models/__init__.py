from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

"""
    Registering Tables in the database
"""

from .usermodel import User
from .idp_users_model import idp_users