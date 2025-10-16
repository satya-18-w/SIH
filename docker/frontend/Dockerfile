# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install poetry


COPY frontend/requirements.txt ./
RUN pip install --no-cache-dir --timeout=600 -r requirements.txt

# Command to run the application
CMD ["streamlit", "run", "frontend/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
