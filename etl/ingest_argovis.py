import requests
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from app.db.session import engine
from app.db.models import Base, Float, Profile, Observation
from app.services.vector_db_adapter import VectorDBAdapter

ARGOVIS_API_URL = "https://argovis.colorado.edu"

def get_db_session():
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()

def ingest_data(days_to_backfill: int = 1):
    """
    Main function to ingest data from the ArgoVis API.
    """
    print(f"Starting data ingestion for the last {days_to_backfill} days...")
    db = get_db_session()
    vector_db = VectorDBAdapter()

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Fetch profiles from the last 24 hours
    try:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days_to_backfill)
        response = requests.get(f"{ARGOVIS_API_URL}/profiles?startDate={start_date.isoformat()}Z&endDate={end_date.isoformat()}Z")
        response.raise_for_status()
        profiles_data = response.json()

        for profile in profiles_data:
            wmo_number = int(profile['platform_number'])

            # Create or get float
            float_obj = db.query(Float).filter_by(wmo_number=wmo_number).first()
            if not float_obj:
                float_obj = Float(
                    wmo_number=wmo_number,
                    platform_type=profile.get('platform_type')
                )
                db.add(float_obj)
                db.commit()

            # Create profile
            profile_summary = f"Profile from float {wmo_number} at {profile['timestamp']}. Mean temp: {profile['bgcMeas'][0].get('temp') if profile.get('bgcMeas') else 'N/A'}"
            profile_obj = Profile(
                float_id=float_obj.id,
                cycle_number=profile['cycle_number'],
                timestamp=pd.to_datetime(profile['timestamp']),
                location=f"SRID=4326;POINT({profile['geolocation']['coordinates'][0]} {profile['geolocation']['coordinates'][1]})",
                profile_summary=profile_summary
            )
            db.add(profile_obj)
            db.commit()

            # Add to vector DB
            vector_db.upsert(
                docs=[profile_obj.profile_summary],
                metadatas=[{"float_id": float_obj.wmo_number, "profile_id": profile_obj.id}],
                ids=[str(profile_obj.id)]
            )

            # Process observations
            if 'measurements' in profile:
                for measurement in profile['measurements']:
                    obs = Observation(
                        profile_id=profile_obj.id,
                        pressure=measurement.get('pres'),
                        temperature=measurement.get('temp'),
                        salinity=measurement.get('psal'),
                    )
                    db.add(obs)
                db.commit()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from ArgoVis: {e}")
        db.rollback()

    db.close()
    print("Data ingestion finished.")

if __name__ == "__main__":
    ingest_data()
