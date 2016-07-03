# Introduction

This script converts comma-separated value (CSV) files of a specific type into KML files.

# Installation instructions

## Ubuntu LTS (14.04 or 16.04)

    sudo apt-get install git python python-kml
    cd ~
    git clone https://github.com/TerryOtt/segmentcsv2kml
    cd segmentcsv2kml
    mkdir -p ~/tmp/kmloutput
    python segmentcsv2kml [url] ~/tmp/kmloutput
    ls -laF ~/tmp/kmloutput

# Licensing

segmentcsv2kml is licensed under the MIT License. Refer to
[LICENSE](https://github.com/TerryOtt/segmentcsv2kml/blob/master/LICENSE) 
for the full license text.
