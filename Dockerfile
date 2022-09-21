# Python image to use.
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

RUN apt-get update -y
# Get's shared library for zbar
RUN apt-get install -y libzbar0
# Installs Python
RUN apt-get install -y python3-pip python3-dev build-essential


COPY requirements.txt .


# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt


# Copy the rest of the working directory contents into the container at /app
COPY . .

# Run app.py when the container launches
ENTRYPOINT ["python", "app.py"]
