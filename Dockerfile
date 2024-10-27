FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV FIREFOX_VER 109.0


# Install Chrome
# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# Updating apt to see and install Google Chrome
RUN apt-get -y update
# Magic happens
RUN apt-get install -y google-chrome-stable


# Install Firefox
RUN apt install -y firefox-esr
RUN set -x \
   && apt install -y \
       libx11-xcb1 \
       libdbus-glib-1-2 \
   && curl -sSLO https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VER}/linux-x86_64/en-US/firefox-${FIREFOX_VER}.tar.bz2 \
   && tar -jxf firefox-* \
   && mv firefox /opt/ \
   && chmod 755 /opt/firefox \
   && chmod 755 /opt/firefox/firefox


# Install dependencies
RUN pip install --no-cache -U pip setuptools pipenv \
    && rm -rf /root/.cache/pip

COPY --chown=1000:1000 ./requirements.txt /opt/automation/

RUN pip install --no-cache -r /opt/automation/requirements.txt \
    && rm -rf /root/.cache/pip
