#!/usr/bin/env python3

import argparse
import sys
import os
import json
from pprint import pprint
import csv


def main():
    args = parseArgs(sys.argv)

    parsedData = readJson(args.jsonFile)
    print( "Read all JSON data successfully" )

    # Debugging to identify structure
    # pprint( parsedData['data']['isolated'] )
    # pprint( parsedData['data']['roadTypes'] )
    # pprint( parsedData['data']['wmeURL'] )

    convertJsonToCsv( parsedData['data']['isolated'], args.csvFile )


def parseArgs(cmdLineArgs):
    parser = argparse.ArgumentParser(description='Convert JSON to CSV for KML conversion')

    parser.add_argument( 'jsonFile', help='Input file containing JSON from segment scan' )
    parser.add_argument( 'csvFile', help='Output file for CSV conversion' )

    return parser.parse_args()


def readJson(jsonFilename):
    try:
        with open(jsonFilename) as jsonFile:
            # File has one top-level object
            return json.load(jsonFile)[0]

    except IOError:
        print( "\nERROR: could not read JSON input file \"{0}\"".format(jsonFilename) )
        sys.exit()

    return None


def convertJsonToCsv( segmentDictionary, csvFilename ):

    # Data comes in a dictionary of lists of dictionaries
    
    # segment type (dictionary key) -> list of dictionaries (one dictionary per segment)
    # valid segment type keys:
    #
    #   15:
    #    6:
    #    3:

    roadTypeMappings = {
        'Street':                1,
        'Primary Street':        2,
        'Freeway':               3,
        # 'Ramp                  4,
        # Walking trail          5,
        'Major Highway':         6,
        'Minor Highway':         7,
        # 'Dirt Road':           8,
        # ???                    9,
        # Pedestrian Boardwalk  10,
        # Ferry:                15,
        # Private Road          17,
        # Railroad              18,
        # Runway/taxiway        19,
        # Parking lot road      20,
        # Service road          21,
    }

    try:
        with open(csvFilename, 'w') as csvFile:
            segmentCsvWriter = csv.writer(csvFile, quoting=csv.QUOTE_ALL)
            addCsvHeaderRow(segmentCsvWriter)
            for currRoadType in [ 'Freeway', 'Major Highway', 'Minor Highway', 'Primary Street', 'Street' ]:
                if str(roadTypeMappings[currRoadType]) not in segmentDictionary:
                    continue
                segmentList = segmentDictionary[ str(roadTypeMappings[currRoadType]) ]
                addPermalinksToSegments(segmentList)
                addSegmentsToCsv( currRoadType, segmentList, segmentCsvWriter)
                print( "Added {0:7d} segments of type {1:13s} (road type #{2})".format(
                    len(segmentList), currRoadType, roadTypeMappings[currRoadType]) )

    except IOError:
        print( "\nERROR: IO error when creating CSV file \"{0}\"".format(csvFilename) )
        sys.exit()


def addPermalinksToSegments(segmentList):
    
    segmentIter = range(len(segmentList))
    for i in range(len(segmentList)):
        segmentList[i]['permalink'] = generatePermalink(segmentList[i])

        #pprint(segmentList[i])


def generatePermalink(segmentDictionary):
    location = segmentDictionary['location']
    segmentId = int(segmentDictionary['segid'])
    lon = float(location['lon'])
    lat = float(location['lat'])
    #print( "Segment {0:12d}: {1:.05f}, {2:.05f}".format(segmentId, lon, lat) )

    protocol =          "https"
    host =              "www.waze.com"
    script =            "editor"
    zoomLevel =         5
    return "{0}://{1}/{2}?zoom={3}&lon={4:.5f}&lat={5:.6f}&segments={6}".format(
        protocol,
        host,
        script,
        zoomLevel,
        lon,
        lat,
        segmentId )


def addCsvHeaderRow(segmentCsvWriter):
    headerRow = [ 'ID', 'PL', 'Road Type', 'FWD Dir', 'FWD Speed', 'REV Dir', 'REV Speed', 'Name', 'City' ]

    segmentCsvWriter.writerow(headerRow)

def addSegmentsToCsv( currRoadType, segmentList, csvWriter ):
    for currSegment in segmentList:

        rowData = [
            currSegment['segid'],               # ID
            currSegment['permalink'],           # PL
            currRoadType,                       # Road type
            "",                                 # FWD Dir
            "",                                 # FWD Speed
            "",                                 # REV Dir
            "",                                 # REV Speed
            "",                                 # Name
            "",                                 # City
        ]

        csvWriter.writerow(rowData)

        if currRoadType != 'Major Highway':
            pprint( currSegment )


if __name__ == '__main__':
    main()
