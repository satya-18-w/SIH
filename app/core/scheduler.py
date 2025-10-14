from apscheduler.schedulers.background import BackgroundScheduler
from etl.ingest_argovis import ingest_data

scheduler = BackgroundScheduler()

def start_scheduler():
    """
    Starts the scheduler to run the data ingestion job daily.
    """
    scheduler.add_job(ingest_data, 'interval', days=1, args=[1])
    scheduler.start()
    print("Scheduler started. Data ingestion will run daily.")
