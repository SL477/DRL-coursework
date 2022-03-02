# Using some hints from https://code.visualstudio.com/docs/containers/quickstart-python
FROM python:3.8-slim-buster

# Expose the port for jupyter-labs
EXPOSE 8890

ADD requirements.txt .

RUN python -m pip install -r requirements.txt