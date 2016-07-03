FROM ubuntu:xenial

MAINTAINER Terry Ott <Terry.Ott@gmail.com>
LABEL Description="Container to test install of segmentcsv2kml"
RUN apt-get update && apt-get -y upgrade

RUN apt-get -y install git python python-kml

WORKDIR /root

RUN git clone https://github.com/TerryOtt/segmentcsv2kml

WORKDIR /root/segmentcsv2kml

CMD /bin/bash
