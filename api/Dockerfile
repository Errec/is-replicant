# Use a slim variant of Python for smaller image size
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user and group
RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup

# Create the NLTK data directory
RUN mkdir -p /app/nltk_data

# Download NLTK data
RUN python -m nltk.downloader -d /app/nltk_data punkt

# Set proper permissions
RUN chown -R appuser:appgroup /app

# Copy the application code
COPY ./app /app/app

# Set the non-root user to run the application
USER appuser

# Set environment variable for NLTK data directory
ENV NLTK_DATA=/app/nltk_data

# Expose the port FastAPI will run on
EXPOSE 8000

# Default command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]