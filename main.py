import csv
import requests

def getDataFromWeb():
    # Simeon
    pass

def writeDataToDB():
    # Parse CSV File and write to respective tables / Columns in DB
    # Select distinct from cols: gender, status, nationality, sector
    # insert in to tables genders, statuses, nationalities, sectors
    # select all from 
    pass

def createTables():
    # Simeon
    genders = '''
        CREATE TABLE GENDERS (
            id INT AUTO_INCREMENT PRIMARY KEY,
            gender VARCHAR(255)
        )
    '''
    nationalities = '''
        CREATE TABLE NATIONALITIES (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nationality VARCHAR(255)
        )
    '''
    sectors = '''
        CREATE TABLE SECTORS (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sector VARCHAR(255)
        )
    '''
    statuses = '''
        CREATE TABLE STATUS (
            id INT AUTO_INCREMENT PRIMARY KEY,
            status VARCHAR(255)
        )
    '''
    dataEntries = '''
        CREATE TABLE DATA_ENTRIES (
            id INT AUTO_INCREMENT PRIMARY KEY,
            status INT,
            sector INT,
            year INT,
            gender INT,
            value INT,
            FOREIGN KEY (status) REFERENCES STATUS(id),
            FOREIGN KEY (sector) REFERENCES SECTORS(id),
            FOREIGN KEY (gender) REFERENCES GENDERS(id)
        )
    '''

    queries = [genders, nationalities, sectors, statuses, dataEntries]

def connectToDB():
    # Louis
    pass
