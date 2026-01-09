# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies (needed for some music/audio libraries if we expand)
# For now, just basic tools
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# expose port 5000 for the flask app
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=web/app.py

# Run main.py web when the container launches
CMD ["python", "main.py", "web"]
