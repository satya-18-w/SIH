from fastapi import APIRouter, BackgroundTasks
from etl.ingest_netcdf import ingest_data

router = APIRouter()

@router.post("/ingest")
def trigger_ingestion(background_tasks: BackgroundTasks):
    """
    Triggers the data ingestion process in the background.
    """
    background_tasks.add_task(ingest_data)
    return {"message": "Data ingestion started in the background."}
