FROM ubuntu:15.04

MAINTAINER Mirko Stocker

RUN apt-get update

RUN apt-get install -y tar git curl nano wget dialog net-tools build-essential

RUN apt-get install -y python python-dev python-distribute python-pip pypy-dev

RUN apt-get install -y libgdal-dev libgdal1-dev python-numpy

ADD . /retrieve-height-service

RUN pip install \
	--global-option=build_ext --global-option="-I/usr/include/gdal" \
	-r /retrieve-height-service/documentation/requirement.txt

EXPOSE 55555
EXPOSE 5000

VOLUME /retrieve-height-service/data

WORKDIR /retrieve-height-service

CMD python run.py
