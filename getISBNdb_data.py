# -*- coding: utf-8 -*-
"""
Created on Sat Feb 09 18:01:44 2013

@author: Anirudh
"""

import xml.etree.ElementTree as ET
import urllib2

access_key = "ZFFYQ5I5"


def getBookDataXML(ISBN, accessKey):
    ''' Returns xml data for a book from www.isbndb.com.
        
    Inputs - ISBN number of book, access_key - provided from isbndb.com after account is created in isbndb.com
    
    Returns data about the book in the form of xml. Check isbndb.com for format'''
    
    bookurl ="http://isbndb.com/api/books.xml?access_key="+accessKey+"&index1=isbn&value1="+ISBN
    isbndbResponse=urllib2.urlopen(bookurl)
    return isbndbResponse.read()

def getBookData(element):
    ''' Extracts book data from an xml element. xml element structure is 
    available at isbndb.com
    
    Return a dictionary containing the following data
    Title
    TitleLong
    Authors
    Publisher
    ISBN
    ISBN13
    '''
    bookDict = {}
    bookDict['ISBN']= element.attrib['isbn']
    bookDict['ISBN13']=element.attrib['isbn13']
    bookDict['Title']=element.find('Title').text
    bookDict['TitleLong']=element.find('TitleLong').text
    bookDict['Author']=element.find('AuthorsText').text
    bookDict['Publisher']=element.find('PublisherText').text
    
    return bookDict
    

def getBookDataFromXML(elementRoot):
    ''' Takes in the xml response from www.isbndb.com and returns book data as 
    dictionary '''
    
    # check how many results were returned
    totalResults = elementRoot.find('BookList').attrib['total_results']
    if totalResults == '1':
        bookListElement = elementRoot.find('BookList')
        return getBookData(bookListElement.find('BookData'))
    elif totalResults == '0':
        #return "No results for this ISBN"
	return None
    else :
        #return "Too many results for the query. Check query or modify code."
        return None


if __name__=="__main__":
    root = ET.parse("test_xml.xml")
    finalDict = {}
    finalDict['DRC_Num']='D01153'
    finalDict.update(getBookDataFromXML(root))
    print finalDict
