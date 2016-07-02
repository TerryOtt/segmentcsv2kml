#!/usr/bin/env python

import sys
import argparse

def main():
    kmlFilename = parseArgs()

def parseArgs():
    parser = argparse.ArgumentParser(description="Convert CSV file with segment data to KML")
    parser.add_argument('csvURL', help='URL to the CSV to download, e.g. "http://db.slickbox.net/states/Ohio-sl.csv")


if __name__ == "__main__":
    main()
