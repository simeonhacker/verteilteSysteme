import csv
import requests

def getDataFromWeb():
    pass

def writeDataToDB():
    # Parse CSV File an dwrite to respective tables / Columns in DB
    pass

def createTables():
    # 
    genders = 'CREATE TABLE GENDERS (id int IDENTITY(1,1) PRIMARY KEY, gender varchar(255))'
    nationalities = 'CREATE TABLE NATIONALITIES (id int IDENTITY(1,1) PRIMARY KEY, nationality varchar(255))'
    sectors = 'CREATE TABLE SECTORS (id int IDENTITY(1,1) PRIMARY KEY, sector varchar(255))'
    status = 'CREATE TABLE STATUS (id int IDENTITY(1,1) PRIMARY KEY, status varchar(255))'
    dataEntries = 'CREATE TABLE dataEntries (id int IDENTITY(1,1) PRIMARY KEY, , year int, gender ,value int)'


    queries = [genders, nationalities, sectors, status]

def connectToDB():
    pass
