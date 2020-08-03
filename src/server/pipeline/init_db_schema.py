from models import Base


def start(connection):
    Base.metadata.create_all(connection)
