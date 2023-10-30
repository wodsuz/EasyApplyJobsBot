FROM python:3.12-alpine

ENV PYTHONUNBUFFERED 1
ENV CHROMEDRIVER_VERSION="114.0.5735.90"

# Install Chromium and its dependencies
RUN apk --no-cache add chromium

# Install specific version of chromedriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver
    
COPY ../requirements.yaml /requirements.yaml
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.yaml

RUN mkdir /app
COPY ./ /app
WORKDIR /app

CMD python3 linkedin.py

# # Install Chromium and its dependencies
# RUN apk --no-cache add chromium udev ttf-freefont

# # Manually download and install chromedriver
# RUN CHROMEDRIVER_VERSION=`chromium-browser --version | awk '{ print $2 }' | sed 's/\..*//'` && \
#     wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
#     unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ && \
#     chmod +x /usr/local/bin/chromedriver

# # Install Chromium and its dependencies
# RUN apk --no-cache add \
#     chromium \
#     udev \
#     ttf-freefont \
#     chromedriver

# # Install dependencies for Google Chrome
# RUN apk update && apk add --no-cache \
#     wget \
#     unzip \
#     fontconfig \
#     ttf-freefont \
#     libxcomposite libxrender libxi libxcursor libxdamage \
#     cups-libs dbus-libs libxrandr glib libxext libxfixes \
#     libblkid libmount libc6-compat

# # Install Google Chrome
# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
#     apk add --no-cache --allow-untrusted google-chrome-stable_current_amd64.deb && \
#     rm google-chrome-stable_current_amd64.deb

# RUN mkdir /app
# COPY ./Docker/app /app
# WORKDIR /app
