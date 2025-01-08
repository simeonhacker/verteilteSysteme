import csv
import requests
import mysql.connector
from mysql.connector import Error
from dataBankSettings import connectionDetails

def getDataFromWeb():
    # Simeon
    url = 'https://dam-api.bfs.admin.ch/hub/api/dam/assets/33426131/master'
    request = requests.get(url)
    with open("data.csv", "wb") as file:
        file.write(request.content)

def writeDataToDB():
    cursor = connectToDB()
    if not cursor:
        return

    # Read CSV file
    with open('data.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        data = list(csv_reader)

    # Extract distinct values
    distinct_genders = set(row['gender'] for row in data)
    distinct_statuses = set(row['status'] for row in data)
    distinct_nationalities = set(row['nationality'] for row in data)
    distinct_sectors = set(row['sector'] for row in data)

    # Insert distinct values and get id mappings
    gender_map = {}
    for gender in distinct_genders:
        cursor.execute("INSERT INTO GENDERS (gender) VALUES (%s)", (gender,))
        cursor.execute("SELECT LAST_INSERT_ID()")
        gender_map[gender] = cursor.fetchone()[0]

    status_map = {}
    for status in distinct_statuses:
        cursor.execute("INSERT INTO STATUS (status) VALUES (%s)", (status,))
        cursor.execute("SELECT LAST_INSERT_ID()")
        status_map[status] = cursor.fetchone()[0]

    nationality_map = {}
    for nationality in distinct_nationalities:
        cursor.execute("INSERT INTO NATIONALITIES (nationality) VALUES (%s)", (nationality,))
        cursor.execute("SELECT LAST_INSERT_ID()")
        nationality_map[nationality] = cursor.fetchone()[0]

    sector_map = {}
    for sector in distinct_sectors:
        cursor.execute("INSERT INTO SECTORS (sector) VALUES (%s)", (sector,))
        cursor.execute("SELECT LAST_INSERT_ID()")
        sector_map[sector] = cursor.fetchone()[0]

    # Insert main data
    for row in data:
        cursor.execute("""
            INSERT INTO DATA_ENTRIES (status, sector, year, gender, value)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            status_map[row['status']],
            sector_map[row['sector']],
            int(row['year']),
            gender_map[row['gender']],
            int(row['value'])
        ))

    cursor.connection.commit()
    cursor.close()
    cursor.connection.close()

def createTables():
    # Simeon
    cursor = connectToDB()
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

    for query in queries:
        cursor.execute(query)

    cursor.connection.commit()  
    cursor.close()
    cursor.connection.close()

def connectToDB():
    try:
        connection = mysql.connector.connect(
            host=connectionDetails['host'],
            user=connectionDetails['user'],
            password=connectionDetails['password'],
            database=connectionDetails['database'],
            allow_local_infile=True
        )
        if connection.is_connected():
            return connection.cursor()
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None
        
if __name__ == "__main__":
    createTables()
    getDataFromWeb()
    writeDataToDB()