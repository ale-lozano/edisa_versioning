FROM python:3.9-slim
# Copy the Python script into the container
COPY versioning.py /versioning.py
# Install any necessary dependencies
RUN pip requests
# Set the entry point to run the Python script
ENTRYPOINT ["python", "/versioning.py"]
