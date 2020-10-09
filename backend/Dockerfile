FROM ubuntu:16.04

LABEL maintainer="Geometalab <geometalab@hsr.ch>"

RUN apt-get update \
	&& apt-get install -y \
	tar git curl nano wget dialog net-tools build-essential \
	python python-dev python-distribute python-pip pypy-dev \
	libgdal-dev libgdal1-dev python-gdal \
	&& rm -rf /var/lib/apt/lists/*

COPY requirement.txt /tmp/requirement.txt
RUN pip install -r /tmp/requirement.txt

COPY requirement-GDAL.txt /tmp/requirement-GDAL.txt
RUN pip install \
	--global-option=build_ext --global-option="-I/usr/include/gdal" \
	-r /tmp/requirement-GDAL.txt

ADD . /retrieve-height-service

EXPOSE 5000

VOLUME /retrieve-height-service/data

WORKDIR /retrieve-height-service

CMD python run.py
