#!/usr/bin/env python

# Copyright (c) 2016 Terry D. Ott. 
#
#   You may use, distribute, and modify this code under the terms
#   of the MIT License.
#
#   You should have received a copy of the MIT License with this
#   file. If not, please visit:
#
#   https://github.com/TerryOtt/segmentcsv2kml/blob/master/LICENSE    
#
#   or
#
#   https://opensource.org/licenses/MIT

import sys
import argparse
import urllib2
import contextlib
import StringIO
import csv
import re
import kmldom
import kmlengine
import os.path

def main():
    (csvURL, kmlDirectory) = parseArgs()

    segmentList = validateAndReadCsvUrl(csvURL)

    print "Read {0} data lines from {1}".format(len(segmentList), csvURL)

    # Create dictionary sorted by segment type
    segmentsByType = createSegmentTypeDictionary(segmentList)

    print "Number of MH: {0}".format(len(segmentsByType['Major Highway']))
    print "Number of mH: {0}".format(len(segmentsByType['Minor Highway']))

    generateKml(segmentsByType, kmlDirectory)

def parseArgs():
    parser = argparse.ArgumentParser(description="Convert CSV file with segment data to KML")
    parser.add_argument('csvURL', 
        help='URL to the CSV to download, e.g. "http://db.slickbox.net/states/Ohio-sl.csv"')
    parser.add_argument('kmlDirectory',
        help='Directory to store generated KML file(s)')

    args = parser.parse_args()

    # Make sure target directory exists
    if os.path.isdir(args.kmlDirectory) is False:
        print "\nERROR: Specified output directory {0} does not exist".format(args.kmlDirectory)
        sys.exit()

    return (args.csvURL, args.kmlDirectory)

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
        for i in range(len(row)):
            segmentDetails[columnHeaders[i]] = row[i]

        # Add the latitude and longitude to the segment details
        (lon, lat) = getLonLatFromPermalink(segmentDetails['PL'])

        segmentDetails['Longitude'] = float(lon)
        segmentDetails['Latitude'] = float(lat)

        # Add to list of segments with segment ID as key
        segmentList[int(row[0])] = segmentDetails

    return segmentList

def getLonLatFromPermalink(segmentPermalink):
    #print "Scanning PL: " + segmentPermalink
    matches = re.search( r'&lon=([-\d\.]+).*&lat=([-\d\.]+)', segmentPermalink)

    return matches.groups()

def createSegmentTypeDictionary(segmentList):

    segmentTypeDictionary = {}

    knownSegmentTypes = []

    for currSegmentId in segmentList:
        if segmentList[currSegmentId]['Road Type'] not in segmentTypeDictionary:
            print "Found new segment type: " + segmentList[currSegmentId]['Road Type']
            segmentTypeDictionary[segmentList[currSegmentId]['Road Type']] = [ segmentList[currSegmentId] ]
        else:
            segmentTypeDictionary[segmentList[currSegmentId]['Road Type']].append(
                segmentList[currSegmentId] )

    return segmentTypeDictionary


def generateKml(segmentsByType, kmlDirectory):

    '''
    Set maximums by what Google MyMaps can display
        10 layers
        2000 features per layer
        max 10,000 elements per file

        Retrieved from: https://support.google.com/mymaps/answer/3370982?hl=en
    '''
    maxKmlFeatures =            10000
    currKmlFeatures =           0
    maxKmlFeaturesPerLayer =    2000
    currKmlLayers =             0
    maxKmlLayers =              10

    kmlFactory = kmldom.KmlFactory_GetFactory()

    doneProcessing = False
    layer = None

    for currLayerType in [ 'Freeway', 'Major Highway', 'Minor Highway' ]:
    #for currLayerType in [ 'Major Highway' ]:

        numberOfLayersForType = 0

        if doneProcessing:
            print "Found we were done processing at layer type loop, bailing"
            break

        if currLayerType not in segmentsByType:
            continue

        for currFeature in segmentsByType[currLayerType]:
            if doneProcessing:
                print "Found we were done processing at the feature loop, bailing"
                break

            # Do we need new layer for this feature?
            if layer == None:

                # Can we create a new layer?
                if ( currKmlLayers < maxKmlLayers ):
                    (layer, numberOfLayersForType, currFeaturesInLayer, currKmlLayers) = \
                        createLayer( kmlFactory, currLayerType, numberOfLayersForType, 
                        currKmlLayers)
                else:
                    print "Cannot create new layer, already at {0} which is max for KML".format(
                        maxKmlLayers)
                    doneProcessing = True
                    break

            placemark = kmlFactory.CreatePlacemark()
            placemark.set_name(currFeature['ID'])
            placemark.set_description(str(currFeature['PL']))
            coordinates = kmlFactory.CreateCoordinates()
            coordinates.add_latlng(currFeature['Latitude'], currFeature['Longitude'] )
            point = kmlFactory.CreatePoint()
            point.set_coordinates(coordinates)
            placemark.set_geometry(point)
            layer.add_feature(placemark)
            placemark = None

            # Increment total features as well as features in layer and see if we hit a limit
            currKmlFeatures += 1
            currFeaturesInLayer += 1

            if currKmlFeatures == maxKmlFeatures or currFeaturesInLayer == maxKmlFeaturesPerLayer:

                (layer, currFeaturesInLayer) = closeLayer( layer, currKmlLayers, 
                    currFeaturesInLayer, kmlFactory, kmlDirectory)

            # Did we hit total feature limit
            if ( currKmlFeatures == maxKmlFeatures):
                print "Hit limit of {0} features per KML file".format(maxKmlFeatures)
                doneProcessing = True
                break
                
        if ( currFeaturesInLayer > 0 and not doneProcessing ):
            (layer, currFeaturesInLayer) = closeLayer(layer, currKmlLayers,
                currFeaturesInLayer, kmlFactory, kmlDirectory)


def closeLayer(layer, currKmlLayers, currFeaturesInLayer, kmlFactory, kmlDirectory):

    print "Closing layer {0} with {1} elements".format(
         layer.get_name(), currFeaturesInLayer)

    # Create KML document to store layer in
    kmlDocument = kmlFactory.CreateDocument()
    kmlDocument.add_feature(layer)

    # Write document out
    with open("{0}/{1:02d}_{2}.kml".format(
        kmlDirectory, currKmlLayers, 
        layer.get_name().replace(' ', '_')), 'w') as kmlFile:

        kmlFile.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n' +
            kmldom.SerializePretty(kmlDocument) + '</kml>' )

    layer = None
    currFeaturesInLayer = 0

    return (layer, currFeaturesInLayer)

def createLayer(kmlFactory, currLayerType, numberOfLayersForType, currKmlLayers):
    layer = kmlFactory.CreateFolder()
    numberOfLayersForType += 1
    currFeaturesInLayer = 0
    currKmlLayers += 1

    currLayerName = "{0} {1:02d}".format(currLayerType, numberOfLayersForType)
    layer.set_name(currLayerName)

    print "\nCreated layer " + currLayerName

    return (layer, numberOfLayersForType, currFeaturesInLayer, currKmlLayers)
    
        
if __name__ == "__main__":
    main()
