from app.db.session import engine
from app.db.models import Base

def create_db_and_tables():
    """
    Creates the database and all tables.
    """
    Base.metadata.create_all(bind=engine)
