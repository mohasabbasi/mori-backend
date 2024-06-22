# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN  apt-get install git-all 
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
