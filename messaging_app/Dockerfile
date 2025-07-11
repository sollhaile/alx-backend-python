# Use official Python image as base
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Collect static files (if your app uses them)
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Run the app with gunicorn
CMD ["gunicorn", "messaging_app.wsgi:application", "--bind", "0.0.0.0:8000"]
