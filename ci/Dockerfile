FROM artifacts.corp.zoom.us/zoom-docker-virtual/zoombase/ubuntu/python3
COPY . /app-src
RUN pip install /app-src --index-url https://artifacts.corp.zoom.us/artifactory/api/pypi/zoom-pypi-virtual/simple
EXPOSE 8000
CMD ["uvicorn", "zdt_datagenie.main:app", "--host", "0.0.0.0", "--port", "8000"]
