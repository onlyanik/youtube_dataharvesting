import streamlit as st
import mysql.connector
import pandas as pd

# Replace these values with your MySQL connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'india123',
    'database': 'IITM_youtube_dataharvesting'
}

# Connect to MySQL
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Retrieve all data from a specific column
column_name = 'channel_name'  # Replace with your actual column name
query = f'SELECT DISTINCT {column_name} FROM youtube_data'
cursor.execute(query)

# Fetch all distinct values from the specified column
distinct_values = [row[0] for row in cursor.fetchall()]

# Close the cursor and connection
cursor.close()
connection.close()

# Streamlit app
st.title('MySQL Data Selection and Display')

# Select a value from the specified column
selected_value = st.selectbox(f'Select a value from {column_name}', distinct_values)

# Connect to MySQL again to fetch row data based on the selected value
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Fetch all data for the selected value
query = f'SELECT * FROM youtube_data WHERE {column_name} = %s'
cursor.execute(query, (selected_value,))
selected_data = cursor.fetchall()

# Close the cursor and connection
cursor.close()
connection.close()

# Display the selected data in a table
st.table(pd.DataFrame(selected_data, columns=[desc[0] for desc in cursor.description]))
