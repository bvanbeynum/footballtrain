FROM python:3.8

RUN mkdir /working

WORKDIR /working

RUN apt-get update

run python -m pip install --upgrade pip
RUN pip install numpy
RUN pip install matplotlib
RUN pip install tensorflow
RUN pip install sklearn

CMD ["python"]