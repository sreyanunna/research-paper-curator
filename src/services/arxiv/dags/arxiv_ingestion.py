# airflow/dags/arxiv_ingestion.py
from datetime import datetime, timedelta
from airflow.decorators import dag, task


@dag(
    schedule="0 6 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,                       # no backfill stampede
    max_active_runs=1,                   # no overlapping runs
    default_args={"retries": 2, "retry_delay": timedelta(minutes=30)},
    tags=["arxiv"],
)
def arxiv_paper_ingestion():

    @task
    def ingest():
        # Import INSIDE the task, not at module top.
        from src.services.metadata_fetcher import run_ingestion
        return run_ingestion(max_results=5)

    ingest()


arxiv_paper_ingestion()