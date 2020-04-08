FROM python:3.8

RUN echo "deb [trusted=yes] http://www.deb-multimedia.org buster main non-free" >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get --assume-yes install deb-multimedia-keyring
RUN apt-get update
RUN apt-get --assume-yes install ffmpeg

RUN pip install requests

WORKDIR /usr/src

CMD ["python"]