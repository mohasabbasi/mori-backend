# Use an official Ubuntu runtime as a parent image
FROM ubuntu:22.04

# Update and install dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    gcc \
    python3-pip \
    git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python packages
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install ftfy regex tqdm
RUN pip install git+https://github.com/openai/CLIP.git
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the data extraction script
RUN python3 data/etl.py

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV QDRANT_URL=http://qdrant.mori-ai.svc:6333

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
