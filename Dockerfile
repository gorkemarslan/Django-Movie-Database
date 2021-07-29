# Pull base image
FROM python:3.9.6
# Set environment variables
# Python will not try to write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it
ENV PYTHONUNBUFFERED 1
# Set work directory
WORKDIR /code
# Add requirements.txt file to container
ADD requirements.txt /code/
# Install requirements
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt
RUN pip install coverage flake8
# Copy project
COPY . /code/