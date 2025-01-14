# Pull an Image
FROM python:3.10.4-slim-bullseye

# Environment Variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Define the working directory
WORKDIR /code

# Copy the dependencies file and install them
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy the rest of the project files
COPY . /code