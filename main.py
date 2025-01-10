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
    connection = connectToDB()
    cursor = connection.cursor()
    if not cursor:
        return
    
    # ensure tables are empty
    cursor.execute("DELETE FROM DATA_ENTRIES")
    cursor.execute("DELETE FROM STATUS")
    cursor.execute("DELETE FROM SECTORS")
    cursor.execute("DELETE FROM GENDERS")
    cursor.execute("DELETE FROM NATIONALITIES")

    connection.commit()  # Commit the deletions


    # Read CSV file
    with open('data.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        data = list(csv_reader)

    # Extract distinct values
    distinct_genders = set(row['GENDER_DE'] for row in data)
    distinct_statuses = set(row['STATUS'] for row in data)
    distinct_nationalities = set(row['NAT_DE'] for row in data)
    distinct_sectors = set(row['DETAILS_DE'] for row in data)

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
        value = None if not row['VALUE'] else int(float(row['VALUE']))
        cursor.execute("""
            INSERT INTO DATA_ENTRIES (status, sector, year, gender, value)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            status_map[row['STATUS']],
            sector_map[row['DETAILS_DE']],
            int(row['PERIOD']),
            gender_map[row['GENDER_DE']],
            value
        ))

    connection.commit()
    cursor.close()
    connection.close()

def createTables():
    # Simeon
    genders = '''
        CREATE TABLE IF NOT EXISTS GENDERS (
            id INT NOT NULL AUTO_INCREMENT,
            gender VARCHAR(255),
            PRIMARY KEY (id)
        )
    '''
    nationalities = '''
        CREATE TABLE IF NOT EXISTS NATIONALITIES (
            id INT NOT NULL AUTO_INCREMENT,
            nationality VARCHAR(255),
            PRIMARY KEY (id)
        )
    '''
    sectors = '''
        CREATE TABLE IF NOT EXISTS SECTORS (
            id INT NOT NULL AUTO_INCREMENT,
            sector VARCHAR(255),
            PRIMARY KEY (id)
        )
    '''
    statuses = '''
        CREATE TABLE IF NOT EXISTS STATUS (
            id INT NOT NULL AUTO_INCREMENT,
            status VARCHAR(255),
            PRIMARY KEY (id)
        )
    '''
    dataEntries = '''
        CREATE TABLE IF NOT EXISTS DATA_ENTRIES (
            id INT NOT NULL AUTO_INCREMENT,
            status INT,
            sector INT,
            year INT,
            gender INT,
            nationality INT,
            value INT,
            FOREIGN KEY (status) REFERENCES STATUS(id),
            FOREIGN KEY (sector) REFERENCES SECTORS(id),
            FOREIGN KEY (gender) REFERENCES GENDERS(id),
            FOREIGN KEY (nationality) REFERENCES NATIONALITIES(id),
            PRIMARY KEY (id)
        )
    '''

    queries = [genders, nationalities, sectors, statuses, dataEntries]
    
    for query in queries:
        connection = connectToDB()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()  
        connection.close()
    
def connectToDB():
    try:
        connection = mysql.connector.connect(**connectionDetails)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None
        
if __name__ == "__main__":
    createTables()
    getDataFromWeb()
    writeDataToDB()