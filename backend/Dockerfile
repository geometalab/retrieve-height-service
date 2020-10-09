# contains gdal 3.1.3
#  Should be same as FROM osgeo/gdal:ubuntu-full-3.1.3
FROM osgeo/gdal:ubuntu-full-3.1.3

LABEL maintainer="Geometalab <geometalab@hsr.ch>"

RUN apt-get update \ 
	&& apt-get install -y wget locales python3-pip netbase \
	&& rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=rununbuffered \
	LC_ALL=C.UTF-8 \
	LANG=C.UTF-8 \
	LANGUAGE=C.UTF-8 \
	PYTHONFAULTHANDLER=1 \
	PYTHONHASHSEED=random \
	PYTHONIOENCODING=utf-8 \
	PIP_NO_CACHE_DIR=off \
	PIP_DISABLE_PIP_VERSION_CHECK=on \
	PIP_DEFAULT_TIMEOUT=100 \
	POETRY_VERSION=1.1.1

RUN echo "C.UTF-8 UTF-8" > /etc/locale.gen \
	&& locale-gen

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
	&& tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
	&& rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN pip3 install "poetry==$POETRY_VERSION" \
	&& poetry config virtualenvs.create false

LABEL maintainer="Geometalab <geometalab@hsr.ch>"

WORKDIR /retrieve-height-service
COPY poetry.lock pyproject.toml /retrieve-height-service/
RUN poetry install
ADD . /retrieve-height-service

EXPOSE 5000

VOLUME /retrieve-height-service/data

WORKDIR /retrieve-height-service

CMD python run.py
