# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 00:29:37 2013

@author: Anirudh
"""

import urllib2
#import simplejson as json
import json
import time

googleAPIKey='AIzaSyDdbvoEQFRJcB6fo1s5yHto7W31NboTGlg'

def getGoogleResult(ISBN='9780309085496', printCheck=0):
    bookUrl = "https://www.googleapis.com/books/v1/volumes?q=isbn:"+ISBN+\
            "&key="+googleAPIKey
    try :
        googleResponse= urllib2.urlopen(bookUrl)
    except urllib2.URLError, e:
        z = e
        print z
    response =  googleResponse.read()
    if printCheck:
        print response
    return response
    
def lineToList(line):
    "Returns a line read from a csv file as a list"
    lineList = []  
    for elem in (line.strip('\n')).split(','):
        lineList.append(elem)
    return lineList


def readCSVFile(filename):
    " Reads a csv file line by line and converts each line to a list"
    csvFile = open(filename, 'r')
    for line in csvFile.readlines():
        #print lineToList(line)
        csvLineList = lineToList(line)
        getGoogleResult(csvLineList[0])
        
    
def getCount(fileName):
    csvFile = open(fileName, 'r')
    Total_count = 0
    found_count = 0
    for line in csvFile.readlines():
        Total_count = Total_count + 1
        csvLineList=lineToList(line)
        bookJson = json.loads(getGoogleResult(csvLineList[0]))
        if bookJson['totalItems'] == 1:
            found_count = found_count + 1
            csvLineList.append('Found')
            print csvLineList
        else :
            csvLineList.append('Not Found')
            print csvLineList
        time.sleep(1)
        print Total_count, found_count
    return Total_count, found_count
         
         
def getVolumeInfo(bookJson, ISBN):
    ''' Returns a dict object from a json.loads python object. The json response
    is obtained from google books api '''
    #check if the number of items is 1 (Need to modify later for multiple items)
    bookInfoDict = {} #final dict object to be returned
    if bookJson['totalItems']==1:
        #get the bookItem. bookJson['items'] is a list of book items returned for
        #the query. Only 1 item is returned, hence making it the default item
        bookItem = bookJson['items'][0]
        volumeInfo = bookItem['volumeInfo']

        try:
            bookInfoDict['title']=volumeInfo['title']
        except KeyError:
            print "Unable to find key 'title' "
            bookInfoDict['title']=""
        
        try:
            bookInfoDict['subtitle']=volumeInfo['subtitle']
        except KeyError:
            bookInfoDict['subtitle']=""
            print "Unable to find key 'subtitle'"
            
        try:
            bookInfoDict['authors']=';'.join(volumeInfo['authors'])
        except KeyError:
            bookInfoDict['authors']=""
            print "Unable to find key 'authors'"
            
        try:  
            for ind_identifier in volumeInfo['industryIdentifiers']:
                if ind_identifier['type'] == 'ISBN_10':
                    bookInfoDict['isbn'] = ind_identifier['identifier']
                elif ind_identifier['type']=='ISBN_13':
                    bookInfoDict['isbn13']= ind_identifier['identifier']
                else:
                    bookInfoDict['isbn']='0000000000'
                    bookInfoDict['isbn13']='0000000000000'
        except KeyError:
            bookInfoDict['isbn']='0000000000'
            bookInfoDict['isbn13']='0000000000000'
            print "Unable to find key 'industryIdentifiers'"
            
        try:
            bookInfoDict['categories'] = ';'.join(volumeInfo['categories'])
        except KeyError:
            print "Unable to find key 'categories"
            bookInfoDict['categories']=""
        try:
            bookInfoDict['publisher']=volumeInfo['publisher']
        except KeyError:
            print "Unable to find key 'publisher'"
            bookInfoDict['publisher']=""
        try:
            bookInfoDict['publishedDate']=volumeInfo['publishedDate']
        except KeyError:
            bookInfoDict['publishedDate']=""
            print "Unable to find key 'publishedDate'"
    elif bookJson['totalItems']==0:
        print "Query has 0 items for " + ISBN
    else:
        print "Query has more than 1 item or 0 items. Modify code or stop"
    return bookInfoDict
             
    
def getInfoFromISBN(isbn='9780309085496', printCheck=0):
    bookJson = json.loads(getGoogleResult(isbn, printCheck))
    if printCheck:
        print bookJson
    return getVolumeInfo(bookJson, isbn)
    
def writeToFile(bookDict, filename, fileMode='a'):
    ''' Appends a new bookDict to the given file. 
        Output line is in csv format in the following order
        isbn13, isbn, authors, title, titleLong(title + subtitle), publisher, 
        publishedDate, categories
    '''
    
    if bookDict['subtitle']:
        bookDict['titleLong'] = '\"'+bookDict['title']+': '+bookDict['subtitle']+'\"'
        bookDict['title'] = '\"'+bookDict['title']+'\"'
    else:
        bookDict['title'] = '\"'+bookDict['title']+'\"'
        bookDict['titleLong'] = bookDict['title']
    
    print bookDict
    writeOutOrder = ['isbn13', 'isbn', 'title','titleLong','authors', 'publisher',
                     'publishedDate', 'categories']
    fileOutLine = ','.join([bookDict[i] for i in writeOutOrder])
    print fileOutLine
    ouf = open(filename, fileMode)
    try :
        ouf.write(fileOutLine)
        ouf.write('\n')
    except IOError:
        print "Unable to write to file - " + filename
    ouf.close()
    
def createEmptyFile(filename):
    f = open('filename', 'w')
    f.close()

if __name__=="__main__" :
    
    print getInfoFromISBN('9788131708415', 1)    
    exit()    
    filename = "temp_output.csv"
    fileMode = 'a'
    createEmptyFile(filename)
    try:
        inp = open('my_bookList.csv', 'r')
    except IOError:
        print "Unable to open input file"
        exit()
    for line in inp.readlines():
        lineList = lineToList(line)
        print lineList
        bookDict = getInfoFromISBN(lineList[0])
        if bookDict:
            writeToFile(bookDict,filename, fileMode)
        else:
            fileOutLine = lineList[0] + ",No Data"
            
    