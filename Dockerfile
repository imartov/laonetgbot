# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "python app.py && celery -A celery_app beat -l info && celery -A celery_config worker -l info --concurrency=1 -P solo"]