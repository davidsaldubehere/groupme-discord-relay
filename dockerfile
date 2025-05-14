# Use official Python image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy only requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY main.py ./

# Expose port for Flask/Waitress
EXPOSE 8080

# Run the relay script
CMD ["python", "main.py"]