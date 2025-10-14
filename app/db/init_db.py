from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Profile
from etl.ingest_argovis import ingest_data

def initial_data_load():
    """
    Checks if the database is empty and performs an initial data load if it is.
    """
    db = SessionLocal()
    try:
        # Check if there is any data in the Profile table
        if db.query(Profile).count() == 0:
            print("No data found in the database. Performing initial data load for the last 30 days...")
            ingest_data(days_to_backfill=30)
            print("Initial data load complete.")
        else:
            print("Database already contains data. Skipping initial data load.")
    finally:
        db.close()
