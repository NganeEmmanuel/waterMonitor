from Database.database import Base, engine
from model import user
from model import source
from model import quality
from model import complaint


def create_tables():
    Base.metadata.create_all(engine)

