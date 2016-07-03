# Introduction

This script converts comma-separated value (CSV) files of a specific type into KML files.

# Installation instructions

The only two __supported__ build environments for segmentcsv2kml are Ubuntu Linux or via a 
Docker contain.  

Instructions *may* be provided for other Linux distributions or operating systems, but they are not
supported and very lightly tested, if at all.

## Ubuntu 

Recent Ubuntu releases (12.04 and later) were kind enough to put releases of Google's libkml into
the apt repositories, so we can easily leverage them.

    sudo apt-get install git python python-kml
    cd ~
    git clone https://github.com/TerryOtt/segmentcsv2kml
    cd segmentcsv2kml
    mkdir -p ~/tmp/kmloutput
    python segmentcsv2kml [url] ~/tmp/kmloutput
    ls -laF ~/tmp/kmloutput

## Docker

Instructions on how to install Docker are outside the scope of this document. Please consult
the official [Docker installation documentation](https://docs.docker.com/engine/installation/)
on how to get the Docker environment installed. 

Once Docker is installed, change to the <code>install/</code> directory, and run:

    docker build -t segmentcsv2kml -f Dockerfile .
    docker run -it segmentcsv2kml .

## CentOS

The CentOS/RHEL yum repositories do not include libkml, so we have to compile it.

    sudo yum -y install gcc-c++ zlib-devel libtool expat-devel git libcurl-devel python-devel swig make
    cd ~
    git checkout https://github.com/google/libkml
    cd libkml
    mkdir build
    ./autogen.sh
    ./configure --prefix=/usr/local --disable-java --enable-python
    make 
    make check
    sudo make install

# Running

Create a directory for the output files (e.g., <code>mkdir ~/tmp/speed-kml</code> then:

    python segmentcsv2kml.py [url to CSV file for your state's speed limit data] [directory for KML files]

# Creating A Map

1. Log into [Google MyMaps](https://google.com/maps/d)
1. Create a new map
1. Click the blue *Import* link under "Untitled Layer"
1. Select the first KML (filename starts with "01")
1. Let the system chew on that
1. Once the points for the layer are loaded, disable the layer (click the checkbox)
1. Click *Add layer* button
1. Click the blue *Import* link under the new "Untitled Layer"
1. Select second KML file (file will start with "02")
1. Repeat steps 7-9 until all KML files are uploaded (in order by filename)
1. Re-enable all layers starting at the bottom layer and working your way up


# Licensing

segmentcsv2kml is licensed under the MIT License. Refer to
[LICENSE](https://github.com/TerryOtt/segmentcsv2kml/blob/master/LICENSE) 
for the full license text.
