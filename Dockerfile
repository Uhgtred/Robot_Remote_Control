FROM ubuntu:24.04
LABEL authors="Markus"

# set timezone
ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get install -y python3-venv && \
    apt-get install libevdev2 && \
    apt-get install -y python3-tk && \
    apt-get install -y xvfb && \
    apt-get install -y ffmpeg libsm6 libxext6 && \
    apt-get install -y libgl1 && \
    apt-get install -y libglx-mesa0 && \
    rm -rf /var/lib/apt/lists/*

# Defining a dummy display for headless execution
ENV DISPLAY=:99

# Copy requirements to app-folder
COPY requirements.txt /app/
WORKDIR /app/

# open specified port to the outside
ENV PORT=2000
EXPOSE 2000

# Install dependencies
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip3 install --upgrade pip && \
    /app/venv/bin/pip3 install -r /app/requirements.txt

# Copy SourceCode to app-folder
COPY . /app/

## set environment for python-version
ENV PATH="/app/venv/bin:${PATH}"

# Create symbolic links for coverage commands in /usr/local/bin
RUN ln -sf /app/venv/bin/coverage /usr/local/bin/coverage && \
    ln -sf /app/venv/bin/coverage-3 /usr/local/bin/coverage-3
