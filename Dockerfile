FROM python:3.9-slim
# Copy the Python script into the container
COPY my_script.py /versioning.py
# Install any necessary dependencies
# Set the entry point to run the Python script
ENTRYPOINT ["python", "/versioning.py"]
