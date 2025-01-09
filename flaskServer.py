from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error
import plotly.graph_objs as go
import pandas as pd
from dataBankSettings import connectionDetails

app = Flask(__name__)

def fetchDataFromDB():
    try:
        connection = mysql.connector.connect(**connectionDetails)
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            # Example query: Fetching data from DATA_ENTRIES table
            query = """
            SELECT year, GENDERS.gender, SUM(value) AS total_value
            FROM DATA_ENTRIES
            INNER JOIN GENDERS ON DATA_ENTRIES.gender = GENDERS.id
            GROUP BY year, GENDERS.gender
            ORDER BY year ASC;
            """
            cursor.execute(query)
            data = cursor.fetchall()
            print(data)
            cursor.close()
            connection.close()
            return data
    except Error as e:
        print(f"Error fetching data from database: {e}")
        return []

@app.route('/')
def index():
    # Fetch data
    db_data = fetchDataFromDB()
    
    # Convert data to a DataFrame for easier manipulation
    df = pd.DataFrame(db_data)
    print(df.columns)
    
    # Create a Plotly chart
    fig = go.Figure()

    # Add traces for each gender
    for gender in df['gender'].unique():
        gender_data = df[df['gender'] == gender]
        fig.add_trace(go.Scatter(
            x=gender_data['year'],
            y=gender_data['total_value'],
            mode='lines+markers',
            name=gender
        ))

    # Customize the layout
    fig.update_layout(
        title="Data Entries Over Time by Gender",
        xaxis_title="Year",
        yaxis_title="Total Value",
        template="plotly_dark"
    )

    # Render the chart in the Flask template
    return render_template('index.html', plot=fig.to_html())

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')