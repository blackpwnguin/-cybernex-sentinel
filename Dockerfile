# Use an official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy local files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Start the app
CMD ["python", "backend.py"]
