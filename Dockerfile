FROM python:3.11-slim

WORKDIR /app

# Install required packages
RUN pip install matplotlib numpy argparse

# Copy the Python script
COPY skill_will_quadrant.py .

# Create a directory for output files
RUN mkdir -p /app/output

# Set the working directory as a volume
VOLUME /app/output

# Set the entrypoint
ENTRYPOINT ["python", "skill_will_quadrant.py"]
