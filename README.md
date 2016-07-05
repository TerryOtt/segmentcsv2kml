# Introduction

This script converts comma-separated value (CSV) files of a specific type into KML files.

# Installation instructions

The only two __supported__ environments to run segmentcsv2kml are Ubuntu Linux (14.04 or newer) or Docker.

Instructions *may* be provided for other Linux distributions or operating systems, but they are not
supported and very lightly tested, if at all.

## Ubuntu 16.04 LTS (Xenial)

    sudo apt-get install git python3 python3-pip python3-shapely python3-lxml python3-fastkml 
    cd ~
    git clone https://github.com/TerryOtt/segmentcsv2kml
    cd segmentcsv2kml
    mkdir -p [output directory]
    python segmentcsv2kml [url] [output directory]

## Ubuntu 14.04 LTS (Trusty)

    sudo apt-get install git python3 python3-pip python3-shapely python3-lxml 
    sudo pip3 install fastkml
    cd ~
    git clone https://github.com/TerryOtt/segmentcsv2kml
    cd segmentcsv2kml
    mkdir -p [output directory]
    python segmentcsv2kml [url] [output directory]

## Ubuntu 12.04 LTS (Precise)

These instructions are quite a bit more complicated than others. Due to multiple issues
(can't install Docker or a new enough version of Python 3), we install a Ubuntu 16.04 
virtual machine (VM) using Vagrant and then install segmentcsv2kml inside of that.

    sudo install -y vagrant
    vagrant init hashicorp/xenial64
    vagrant up
    vagrant ssh
    [Continue with Ubuntu 16.04 instructions above]

## CentOS 7.x

    yum update
    yum install epel-release
    yum y install python34 python34-devel geos-python libxml2-devel libxslt-devel yum install gcc gcc-c++ make openssl-devel git zlib-devel
    cd /root
    curl -O https://bootstrap.pypa.io/get-pip.py
    /usr/bin/python3.4 get-pip.py
    pip3.4 install shapely lxml fastkml
    git clone https://github.com/TerryOtt/segmentcsv2kml
    cd segmentcsv2kml
    git checkout python3_investigation
    

## Docker

Instructions on how to install Docker are outside the scope of this document. Please consult
the official [Docker installation documentation](https://docs.docker.com/engine/installation/)
on how to get the Docker environment installed. 

Once Docker is installed, change to the <code>install/</code> directory, and run:

    docker build -t segmentcsv2kml -f Dockerfile .
    docker run -it segmentcsv2kml 

The build steps already downloaded and installed the program, so once you're at the 
bash shell inside the running container, just run the script:

    mkdir -p [output directory]
    python segmentcsv2kml [url] [output directory]

## CentOS

## Windows 


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

segmentcsv2kml is licensed under the [MIT License](https://en.wikipedia.org/wiki/MIT_License). Refer to
[LICENSE](https://github.com/TerryOtt/segmentcsv2kml/blob/master/LICENSE) 
for the full license text.
