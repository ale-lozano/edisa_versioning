FROM python:3.9-slim
# Copy the Python script into the container
COPY versioning.py /versioning.py
# Install Git
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

RUN git config --global safe.directory '*'
RUN git config --global --add safe.directory /github/workspace

# Install any necessary dependencies
RUN pip install requests
# Set the entry point to run the Python script
ENTRYPOINT ["python", "/versioning.py"]
