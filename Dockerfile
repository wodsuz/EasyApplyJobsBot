FROM python:3.12-alpine

# Define build-time variables
ARG CONFIG_FILE

ENV PYTHONUNBUFFERED=1 \
    CHROMEDRIVER_VERSION=114.0.5735.90 \
    # Ensure pip is up to date
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Define the path where the app will be installed
    PATH="/app:${PATH}"

RUN apk add --no-cache chromium chromium-chromedriver

# Create symbolic links for the expected Google Chrome names to the Chromium executable
RUN ln -s /usr/bin/chromium-browser /usr/bin/google-chrome && \
    ln -s /usr/bin/chromium-browser /usr/bin/google-chrome-stable && \
    ln -s /usr/bin/chromium-browser /usr/bin/google-chrome-beta && \
    ln -s /usr/bin/chromium-browser /usr/bin/google-chrome-dev
    
# Copy the requirements file and install Python dependencies
COPY ./requirements.yaml /requirements.yaml
RUN pip install --upgrade pip && pip install -r /requirements.yaml

# RUN mkdir /app

# Copy the application files
COPY . /app

# Copy the specific config file passed in via build argument and rename it to config.py
COPY ./configs/${CONFIG_FILE} /app/config.py

# Set read/write permissions for the data directory
RUN chmod -R 777 /app/data

# Set the working directory
WORKDIR /app

# Use an unprivileged user to run the app
RUN adduser -D user
USER user

CMD ["python3", "linkedin.py"]
