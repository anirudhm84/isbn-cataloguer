# -*- coding: utf-8 -*-
"""
Created on Sat Feb 09 20:44:45 2013

@author: Anirudh
"""

#import urllib2
import xml.etree.ElementTree as ET

from getISBNdb_data import getBookDataXML, getBookDataFromXML

access_key = "ZFFYQ5I5"

def lineToList(line):
    "Returns a line read from a csv file as a list"
    lineList = []  
    for elem in (line.strip('\n')).split(','):
        lineList.append(elem)
    return lineList


def readCSVFile(filename):
    " Reads a csv file line by line and converts each line to a list"
    csvFile = open(filename, 'r')
    #create failList - for those that had no isbndb data
    failList = []
    for line in csvFile.readlines():
        #print lineToList(line)
        csvLineList = lineToList(line)
        bookXML = getBookDataXML(csvLineList[0], access_key)
        bookXMLTree = ET.fromstring(bookXML)
        #print bookXML
        if (getBookDataFromXML(bookXMLTree)):
            print getBookDataFromXML(bookXMLTree)
        else :
            failList.append(csvLineList)
    print len(failList), failList
        


if __name__=="__main__" :
    #readCSVFile('temp_booklist.csv')
    readCSVFile('my_bookList.csv')