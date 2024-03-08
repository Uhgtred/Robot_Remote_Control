FROM ubuntu:latest
LABEL authors="Markus"

# Install python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get install -y python3-venv && \
    apt-get install -y libevdev2 && \
    apt-get install -y python3-tk && \
    apt-get install -y ffmpeg libsm6 libxext6 && \
    apt-get install -y libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements to app-folder
COPY requirements.txt /app/
WORKDIR /app/

# open specified port to the outside
ENV PORT=2000
EXPOSE 2000

# Install dependencies
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip3 install --upgrade pip && \
#    /app/venv/bin/pip3 install evdev && \
    /app/venv/bin/pip3 install -r /app/requirements.txt

# Copy SourceCode to app-folder
COPY ../ /app/

## set environment for python-version
ENV PATH="/app/venv/bin:${PATH}"