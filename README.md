# Introduction

This script converts comma-separated value (CSV) files of a specific type into KML files.

# Installation instructions

The only two __supported__ environments to run segmentcsv2kml are Ubuntu Linux or using a Docker
container built with instructions on this site.  

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
    docker run -it segmentcsv2kml 

The build steps already downloaded and installed the program, so once you're at the 
bash shell inside the running container, just run the script:

    mkdir -p ~/tmp/kmloutput
    python segmentcsv2kml [url] ~/tmp/kmloutput
    ls -laF ~/tmp/kmloutput

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
1. Once the points for the layer are loaded, click the blue "Individual styles" link for the new layer
1. Click on "Group playce by: Individual styles" and select "Uniform style"
1. Click the X for the popup window for layer style info
1. Hover mouse to right of "All items" and click the paintcan icon
1. Select an appropriate color for your pins (e.g., light blue for Major Highway, light green for Minor Highway)
1. Click the X for the popup window for color/icons
1. Repeat for all KML files

Note there is an order pins are drawn. The pins in the first layer listed are drawn first, then 
pins from second layer, etc.

This may mean you want to have your highest Functional Classification layers at the BOTTOM of the list,
so those pins are on top.


# Licensing

segmentcsv2kml is licensed under the [MIT License](https://en.wikipedia.org/wiki/MIT_License). Refer to
[LICENSE](https://github.com/TerryOtt/segmentcsv2kml/blob/master/LICENSE) 
for the full license text.
