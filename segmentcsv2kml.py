#!/usr/bin/env python

import sys
import argparse
import urllib2
import contextlib
import StringIO
import csv
import re
import kmldom
import kmlengine

def main():
    (csvURL, kmlFile) = parseArgs()

    segmentList = validateAndReadCsvUrl(csvURL)

    print "Read {0} data lines from {1}".format(len(segmentList), csvURL)

    # Create dictionary sorted by segment type
    segmentsByType = createSegmentTypeDictionary(segmentList)

    print "Number of MH: {0}".format(len(segmentsByType['Major Highway']))
    print "Number of mH: {0}".format(len(segmentsByType['Minor Highway']))

    generateKml(segmentsByType, kmlFile)

def parseArgs():
    parser = argparse.ArgumentParser(description="Convert CSV file with segment data to KML")
    parser.add_argument('csvURL', 
        help='URL to the CSV to download, e.g. "http://db.slickbox.net/states/Ohio-sl.csv"')
    parser.add_argument('kmlFile',
        help='KML file to generate with output')

    args = parser.parse_args()

    return (args.csvURL, args.kmlFile)

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


def generateKml(segmentsByType, kmlFilename):

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
    numberOfFoldersForType =    0
    currKmlFolders =            0
    maxKmlFolders =             10

    kmlFactory = kmldom.KmlFactory_GetFactory()

    kmlDocument = kmlFactory.CreateDocument()
    kmlDocument.set_name('Generated KML')
    doneProcessing = False
    folder = None

    # for currFolderType in [ 'Freeway', 'Major Highway', 'Minor Highway' ]:
    for currFolderType in [ 'Major Highway' ]:
        if doneProcessing:
            print "Found we were done processing at folder loop, bailing"
            break

        if currFolderType not in segmentsByType:
            continue

        for currFeature in segmentsByType[currFolderType]:
            if doneProcessing:
                print "Found we were done processing at the feature loop, bailing"
                break

            # Do we need a folder for this feature?
            if folder == None:

                # Can we create a new folder?
                if ( currKmlFolders < maxKmlFolders ):
                    (folder, numberOfFoldersForType, currFeaturesInFolder, currKmlFolders) = \
                        createNewFolder( kmlFactory, currFolderType, numberOfFoldersForType,
                        currKmlFolders)
                else:
                    print "Cannot create new folder, already at {0} which is max for KML".format(
                        maxKmlFolders)
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
            folder.add_feature(placemark)
            placemark = None

            # Increment total features as well as features in folder and see if we hit a limit
            currKmlFeatures += 1
            currFeaturesInFolder += 1

            if currKmlFeatures == maxKmlFeatures or currFeaturesInFolder == maxKmlFeaturesPerLayer:

                (kmlDocument, folder, currFeaturesInFolder) = closeFolderAndAddToDocument( folder,
                    kmlDocument, currFeaturesInFolder)

                # testing only, bail as soon as we close first folder
                #doneProcessing = True
                #break

            # Did we hit total feature limit
            if ( currKmlFeatures == maxKmlFeatures):
                print "Hit limit of {0} features per KML file".format(maxKmlFeatures)
                doneProcessing = True
                break
                
        if ( currFeaturesInFolder > 0 and not doneProcessing ):
            (kmlDocument, folder, currFeaturesInFolder) = closeFolderAndAddToDocument(folder, 
                kmlDocument, currFeaturesInFolder)

    with open(kmlFilename, 'w') as kmlFile:
        kmlFile.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n' +
            kmldom.SerializePretty(kmlDocument) + '</kml>' )

def closeFolderAndAddToDocument(folder, kmlDocument, currFeaturesInFolder):

    print "Closing folder {0} with {1} elements".format(
         folder.get_name(), currFeaturesInFolder)
    kmlDocument.add_feature(folder)
    folder = None
    currFeaturesInFolder = 0

    return (kmlDocument, folder, currFeaturesInFolder)

def createNewFolder(kmlFactory, currFolderType, numberOfFoldersForType, currKmlFolders):
    folder = kmlFactory.CreateFolder()
    numberOfFoldersForType += 1
    currFeaturesInFolder = 0
    currKmlFolders += 1

    currFolderName = "{0} Folder #{1}".format(currFolderType, numberOfFoldersForType)
    folder.set_name(currFolderName)
    print "\nCreated folder " + currFolderName

    return (folder, numberOfFoldersForType, currFeaturesInFolder, currKmlFolders)
    
        
if __name__ == "__main__":
    main()
