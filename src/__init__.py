import os, sys

from core.db.session import engine
from src.models import Base

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
def create_tables():
    Base.metadata.create_all(bind=engine)
create_tables()