#!/usr/bin/env python

import sys
import argparse
import urllib2
import contextlib
import StringIO
import csv
import re

def main():
    csvURL = parseArgs()

    segmentList = validateAndReadCsvUrl(csvURL)

    print "Read {0} data lines from {1}".format(len(segmentList), csvURL)

    generateKml(segmentList)

def parseArgs():
    parser = argparse.ArgumentParser(description="Convert CSV file with segment data to KML")
    parser.add_argument('csvURL', 
        help='URL to the CSV to download, e.g. "http://db.slickbox.net/states/Ohio-sl.csv"')

    args = parser.parse_args()

    return args.csvURL

def validateAndReadCsvUrl(url):
    try:
        #return urllib2.urlopen(url).read() 
        urlHandle = urllib2.urlopen(url)

    except urllib2.HTTPError, e:
        print("\nERROR: HTTP error code {0} returned when accessing {1}\n".format(
            e.code, url))
        sys.exit()
    except urllib2.URLError, e:
        print("\nERROR: unable to parse URL {0}, args: {1}\n".format(url, e.args))
        sys.exit()
    except ValueError, e:
        print("\nERROR: Unknown URL type: {0}\n".format(url))
        sys.exit()
    except:
        print("\nERROR: unknown error opening {0}\n".format(url))
        sys.exit()

    csvReader = csv.reader(StringIO.StringIO(urlHandle.read()))

    fileLines = []

    for row in csvReader:
        fileLines.append(row)

    # Remove first row as it's column headers
    columnHeaders = fileLines.pop(0)

    # Create dictionary using column headers for each entry
    segmentList = {}
    for row in fileLines:
        segmentDetails = {}
        for i in range(1, len(row)):

            # Add everything but ID
            segmentDetails[columnHeaders[i]] = row[i]

        # Add the latitude and longitude to the segment details
        (lon, lat) = getLonLatFromPermalink(segmentDetails['PL'])

        print "PL: {0}\n\tLon = {1:f.5}, Lat = {2:f.5}".format(
            segmentDetails['PL'], lon, lat)

        # Add to list of segments with segment ID as key
        segmentList[int(row[0])] = segmentDetails

    return segmentList

def getLonLatFromPermalink(segmentPermalink):
    matches = re.search("&lon=([\d\.]+).*&lat=([\d\.]+)", segmentPermalink)

    return matches.groups()


def generateKml(segmentList):

    print segmentList[83818954]

if __name__ == "__main__":
    main()
