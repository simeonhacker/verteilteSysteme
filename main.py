import csv
import requests

def getDataFromWeb():
    # Simeon
    url = 'https://dam-api.bfs.admin.ch/hub/api/dam/assets/33426131/master'
    request = requests.get(url)
    with open("data.csv", "wb") as file:
        file.write(request.content)

def writeDataToDB():
    pass

def createTables():
    # Simeon
    genders = '''
        CREATE TABLE GENDERS (
            id INT NOT NULL AUTO_INCREMENT,
            gender VARCHAR(255),
            PRIMARY_KEY (id)
        )
    '''
    nationalities = '''
        CREATE TABLE NATIONALITIES (
            id INT NOT NULL AUTO_INCREMENT,
            nationality VARCHAR(255),
            PRIMARY_KEY (id)
        )
    '''
    sectors = '''
        CREATE TABLE SECTORS (
            id INT NOT NULL AUTO_INCREMENT,
            sector VARCHAR(255),
            PRIMARY_KEY (id)
        )
    '''
    statuses = '''
        CREATE TABLE STATUS (
            id INT NOT NULL AUTO_INCREMENT,
            status VARCHAR(255),
            PRIMARY_KEY (id)
        )
    '''
    dataEntries = '''
        CREATE TABLE DATA_ENTRIES (
            id INT NOT NULL AUTO_INCREMENT,
            status INT,
            sector INT,
            year INT,
            gender INT,
            value INT,
            FOREIGN KEY (status) REFERENCES STATUS(id),
            FOREIGN KEY (sector) REFERENCES SECTORS(id),
            FOREIGN KEY (gender) REFERENCES GENDERS(id),
            PRIMARY_KEY (id)
        )
    '''

    queries = [genders, nationalities, sectors, statuses, dataEntries]

def connectToDB():
    # Louis
    pass
