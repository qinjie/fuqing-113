# Use an official Python runtime as a parent image
FROM python:3.9-slim as flask-web

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Create and set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app 
COPY ./app /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose port 5000 for the Flask app to listen on
EXPOSE 5000

# Define the command to run your application
CMD ["flask", "run"]

