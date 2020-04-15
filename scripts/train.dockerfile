FROM python:3.8

RUN apt-get update

RUN pip install numpy
RUN pip install matplotlib
RUN pip install opencv-python
RUN pip install tensorflow

RUN mkdir /working

WORKDIR /working

CMD ["python"]