from config import engine
from models import Base

def start():
    Base.metadata.create_all(engine)
