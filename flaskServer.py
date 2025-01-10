from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error
import plotly.graph_objs as go
import pandas as pd
from dataBankSettings import connectionDetails
import main as db

app = Flask(__name__)

def getDataForPlot():
    connection = db.connectToDB()
    if not connection:
        return None, None

    cursor = connection.cursor()

    # Query distinct years
    cursor.execute("SELECT DISTINCT year FROM DATA_ENTRIES")
    years = cursor.fetchall()
    x_axes1 = [year[0] for year in years]

    y_axes1 = []
    for year in x_axes1:
        cursor.execute("""
            SELECT value FROM DATA_ENTRIES
            JOIN SECTORS ON DATA_ENTRIES.sector = SECTORS.id
            JOIN GENDERS ON DATA_ENTRIES.gender = GENDERS.id
            JOIN NATIONALITIES ON DATA_ENTRIES.nationality = NATIONALITIES.id
            WHERE year = %s AND SECTORS.sector = 'Total' AND GENDERS.gender = 'Total' AND NATIONALITIES.nationality = 'Total'
        """, (year,))
        values = cursor.fetchall()
        y_axes1.extend([value[0] for value in values])

    print(y_axes1)
    print(x_axes1)

    cursor.close()
    connection.close()

    return x_axes1#, y_axes1

if __name__ == "__main__":
    #app.run(debug=True, host='0.0.0.0')
    getDataForPlot()