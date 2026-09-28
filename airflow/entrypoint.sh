#!/bin/bash
set -e

# Create/upgrade Airflow's metadata tables in the `airflow` Postgres database
echo "Migrating Airflow database..."
airflow db migrate

# Airflow 3: runs api-server (UI on :8080), scheduler, dag-processor and triggerer
echo "Starting Airflow standalone..."
exec airflow standalone
