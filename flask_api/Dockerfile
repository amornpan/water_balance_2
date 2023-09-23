# Stage 1: Build the Python dependencies
FROM python:3.9-slim-buster AS builder

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libgdal-dev \
    && apt-get clean

# Set environment variables for GeoPandas
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Install pip and upgrade it
RUN python -m pip install --upgrade pip

# Create a virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install Python dependencies
RUN pip3 install --no-cache-dir Flask Flask-Bootstrap pandas plotly cython geopandas folium pymongo flask-cors

# Stage 2: Create the final image
FROM python:3.9-slim-buster

LABEL version="1.0" \
    name="waterbalance-flask-rest-api"

# Set environment variables for GeoPandas
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Copy the virtual environment from the builder stage
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the rest of your application code into the container
COPY ./flask_api /app

# Specify the command to run your application
CMD ["python3", "app.py", "--host", "0.0.0.0", "--port", "5050"]
