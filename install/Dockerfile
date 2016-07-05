FROM ubuntu:xenial

MAINTAINER Terry Ott <Terry.Ott@gmail.com>
LABEL Description="Container for python3 version of segmentcsv2kml"

RUN apt-get update && apt-get -y upgrade

RUN apt-get -y install git python3 python3-fastkml python3-shapely python3-pip python3-lxml

WORKDIR /root

RUN git clone https://github.com/TerryOtt/segmentcsv2kml

WORKDIR /root/segmentcsv2kml

RUN git pull && git checkout python3_investigation

CMD /bin/bash
