#!/usr/bin/env bash

set -e
echo "BRANCH: ${BRANCH}"
echo "VERSION: ${VERSION}"
echo "Python Version: $(python --version)"

# flake checks
pip install flake8 -i https://artifacts.corp.zoom.us/artifactory/api/pypi/zoom-pypi-virtual/simple
python -m flake8 src --config=ci/.flake8

## Build Docker Image
docker build -t zdt-datagenie -f ci/Dockerfile .
