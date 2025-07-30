# Use an official Python 3.12 runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Update the package list and install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code to the container
COPY . .

# Expose the port that Streamlit will run on. Cloud Run expects 8080 by default.
EXPOSE 8080

# Command to run your Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port", "8080", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]
