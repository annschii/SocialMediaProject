# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app


# Copy only the requirements file first
COPY requirements.txt /app/requirements.txt


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run sentiment_service.py when the container launches
CMD ["python", "sentiment_service.py"]

