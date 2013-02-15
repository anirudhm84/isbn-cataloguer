# -*- coding: utf-8 -*-
"""
Created on Sat Feb 09 17:11:57 2013

@author: Anirudh
"""

import urllib2

access_key = "ZFFYQ5I5"


def getBookDataXML(ISBN, accessKey):
    ''' Returns xml data for a book from www.isbndb.com.
        
    Inputs - ISBN number of book, access_key - provided from isbndb.com after account is created in isbndb.com
    
    Returns data about the book in the form of xml. Check isbndb.com for format'''
    
    bookurl ="http://isbndb.com/api/books.xml?access_key="+accessKey+"&index1=isbn&value1="+ISBN
    isbndbResponse=urllib2.urlopen(bookurl)
    return isbndbResponse.read()


if __name__=="__main__":
    print getBookDataXML("0309085497", access_key)