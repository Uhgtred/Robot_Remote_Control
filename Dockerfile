FROM ubuntu:latest
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
#    apt-get install -y xvfb && \
    apt-get install -y ffmpeg libsm6 libxext6 && \
    apt-get install -y libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements to app-folder
COPY requirements.txt /app/
WORKDIR /app/

# open specified port to the outside
ENV PORT=2000
EXPOSE 2000
ENV DISPLAY :0

# Install dependencies
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip3 install --upgrade pip && \
    /app/venv/bin/pip3 install -r /app/requirements.txt

# Copy SourceCode to app-folder
COPY ../ /app/

# Create a shell script to start xvfb
#RUN echo 'Xvfb :99 -screen 0 1024x768x24 &' > start.sh
#RUN echo 'sleep 3' >> start.sh # Delay needed to give xvfb some time to start
#RUN echo 'python your_script.py' >> start.sh
#RUN chmod +x start.sh

#CMD ["./start.sh"]

## set environment for python-version
ENV PATH="/app/venv/bin:${PATH}"