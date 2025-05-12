# Use official Python image
FROM python:3.13-slim

# Set workdir
WORKDIR /app

# Copy only requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY main.py .env ./

# Expose port for Flask/Waitress
EXPOSE 80

# Run the relay script
CMD ["python", "main.py"]