# Use official Python slim image for smaller size
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy dependencies file first (better Docker layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Expose Flask's default port
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
