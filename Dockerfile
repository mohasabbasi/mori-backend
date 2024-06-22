# Use an official Python runtime as a parent image
FROM ubuntu:22.04
RUN apt-get update && \
    apt-get install --no-install-recommends -y gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/* \
    apt-get install python3-pip

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app


RUN  pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN  pip3 install ftfy regex tqdm
RUN  pip3 install git+https://github.com/openai/CLIP.git
# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

RUN python3 data/etl.py
# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV QDRANT_URL=http://qdrant.mori-ai.svc:6333

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
