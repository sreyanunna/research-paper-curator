FROM apache/airflow:3.0.0-python3.12
# ^ pin to Airflow 3.0.x + Python 3.12 to match your repo and the reference

USER root
# Copy our startup script in and make it runnable.
# Build context is ./airflow (from your compose), so this is ./airflow/entrypoint.sh
COPY entrypoint.sh /opt/airflow/entrypoint.sh
RUN chmod +x /opt/airflow/entrypoint.sh

# Later, when DAGs need your libraries (opensearch-py, sqlalchemy, etc.):
#   USER airflow
#   COPY requirements-airflow.txt /tmp/req.txt
#   RUN pip install --no-cache-dir -r /tmp/req.txt

USER airflow
ENTRYPOINT ["/opt/airflow/entrypoint.sh"]