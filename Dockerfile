# Use the official Python image as the base image
FROM python:3.8-slim

# Install system dependencies for psycopg2-binary, mysqlclient, and pkg-config
RUN apt-get update && \
    apt-get install -y libpq-dev default-libmysqlclient-dev pkg-config gcc

# Set the working directory within the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the required dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that your Flask app runs on
EXPOSE 5000

# Set environment variables (optional)
ENV FLASK_APP=main
ENV FLASK_RUN_PORT=5000
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
