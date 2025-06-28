# Use official Python runtime as a parent image
FROM python:3.10

# Set environment variables to prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the project code into the container
COPY . /app/

# Expose the port that the Django app will run on
EXPOSE 8000

# Run the Django development server on all interfaces (0.0.0.0) at port 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "-p", "8000"]