# Use the official Python image as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port that Flask will run on
EXPOSE 5000

# Define environment variable(s), if needed
# ENV MY_VARIABLE=value

# Command to run the application
CMD ["python", "app.py"]
