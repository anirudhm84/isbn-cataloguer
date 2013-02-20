# -*- coding: utf-8 -*-
"""
Created on Sat Feb 09 20:44:45 2013

@author: Anirudh
"""

#import urllib2
import xml.etree.ElementTree as ET

#from getISBNdb_data import getBookDataXML, getBookDataFromXML, getAccessKey
import getISBNdb_data as isbndb

def lineToList(line):
    "Returns a line read from a csv file as a list"
    lineList = []  
    for elem in (line.strip('\n')).split(','):
        lineList.append(elem)
    return lineList


def readCSVFile(filename, access_key):
    """ Reads a csv file line by line and converts each line to a list. 
        
        Input: filename, isbndb access key """
    csvFile = open(filename, 'r')
    #create failList - for those that had no isbndb data
    failList = []
    for line in csvFile.readlines():
        #print lineToList(line)
        csvLineList = lineToList(line)
        bookXML = isbndb.getBookDataXML(csvLineList[0], access_key)
        bookXMLTree = ET.fromstring(bookXML)
        #print bookXML
        if (isbndb.getBookDataFromXML(bookXMLTree)):
            print isbndb.getBookDataFromXML(bookXMLTree)
        else :
            failList.append(csvLineList)
    print len(failList), failList
        


if __name__=="__main__" :
    #readCSVFile('temp_booklist.csv')
    accessKey = isbndb.GetAccessKey("isbndb_key.txt")
    readCSVFile('my_bookList.csv', accessKey)