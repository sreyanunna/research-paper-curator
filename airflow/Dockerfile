FROM apache/airflow:3.0.0-python3.12
# ^ pin to Airflow 3.0.x + Python 3.12 to match your repo and the reference

USER root
# Copy our startup script in and make it runnable.
# Build context is ./airflow (from your compose), so this is ./airflow/entrypoint.sh
COPY entrypoint.sh /opt/airflow/entrypoint.sh
RUN chmod +x /opt/airflow/entrypoint.sh

USER airflow
# Libraries our DAG tasks need. Pinning apache-airflow stops pip from
# upgrading/downgrading Airflow itself while resolving these. The CPU-only
# PyTorch index keeps docling from pulling multi-GB CUDA wheels.
COPY requirements-airflow.txt /tmp/requirements-airflow.txt
RUN pip install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    "apache-airflow==${AIRFLOW_VERSION}" \
    -r /tmp/requirements-airflow.txt

ENTRYPOINT ["/opt/airflow/entrypoint.sh"]
