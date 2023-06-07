# Use the ARM64 Python base image
FROM arm64v8/python:latest

# Install dependencies required for Chromium and Chrome WebDriver
RUN apt-get update && apt-get install -y chromium-driver

# Set environment variables for Chrome WebDriver
ENV CHROME_DRIVER=/usr/lib/chromium/chromedriver
ENV PATH=$PATH:$CHROME_DRIVER

# Set environment variables for running headless Chromium
ENV DISPLAY=:99

# Install Selenium Python package
RUN pip install selenium

# Set up a working directory inside the container
WORKDIR /app

# Copy your Python application code into the container
COPY test.py .

# Set the entry point for the container
CMD ["python", "test.py"]
