from googleapiclient.discovery import build
import streamlit as st
import pandas as pd
import seaborn as sns
import pymongo
import mysql.connector


# Connection with MySql
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'india123',
    'database': 'IITM_youtube_dataharvesting'
}
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Connection with MongoDB
mongo_host = 'localhost'
mongo_port = 27017
mongo_db_name = 'IITM_youtube_dataharvesting'
mongo_collection_name = 'Capstone_youtubedata'

mongo_client = pymongo.MongoClient(host=mongo_host, port=mongo_port)
mongo_db = mongo_client[mongo_db_name]
mongo_collection = mongo_db[mongo_collection_name]

def xyz():

    #Connecting MongoDB by pymongo

    # client = pymongo.MongoClient("mongodb://localhost:27017")
    # print(client)

    api_key='AIzaSyAQb73Nqw56TKi-aChy0QXES-WQJlH9kvA'
    channel_id='UCX8pnu3DYUnx8qy8V_c6oHg'
    channel_ids=['UCGwWoVeweDVt387NZch_0WQ', # quantz_fintech
                'UCX8pnu3DYUnx8qy8V_c6oHg', #Techno gamers
                'UChfvOaELzzBqDW9oFLG_ztg', #Indian railway fanclub by Satya
                'UCebC4x5l2-PQxg46Ucv9CsA', #crazy xyz by Amit
                'UCj22tfcQrWG7EMEKS0qLeEg', #carry minati
                'UCjvgGbPPn-FgYeguc5nxG4A', #Saurav Joshi Vlogs
                'UCeVMnSShP_Iviwkknt83cww', #Code with Harry
                'UCSiDGb0MnHFGjs4E2WKvShw', # Mr.Indian Hackers
                'UCOhHO2ICt0ti9KAh-QHvttQ', #Technical Guruji
                'UCPxMZIFE856tbTfdkdjzTSQ', # BearBiceps  by Ranbir Allahabadia
                'UCXUJJNoP1QupwsYIWFXmsZg',  #Tech Burner
                ]

    # passing api_service_name, its version and authentication with developer key
    youtube=build('youtube', 'v3', developerKey=api_key)

    #Creating Database in Mongodb
    # db = client['IITM_youtube_dataharvesting']
    # collection = db['Capstone_youtubedata']

    # extracting single channel details
    def get_channel_details(youtube,channel_id):
        request = youtube.channels().list(
            part='snippet,contentDetails,statistics',
            id=channel_id
        )
        response = request.execute()

        data=dict(channel_name = response['items'][0]['snippet']['title'],
                Subscribers=response['items'][0]['statistics']['subscriberCount'],
                Views=response['items'][0]['statistics']['viewCount'],
                Total_videos=response['items'][0]['statistics']['videoCount'],
                Total_likes=response['items'][0]['contentDetails']['relatedPlaylists']['likes'],
                )
        
        return data

    for i in range(len(channel_ids)):

        x=get_channel_details(youtube,channel_ids[i])
        mongo_collection.insert_one(x)


    # the output obtained in json format
        
def transfer_data():
    # Retrieve data from MongoDB
    mongo_data = mongo_collection.find()

    # Transfer data from MongoDB to MySQL
    for document in mongo_data:
        # After creating  column names in MySQL similar to the fields of MongoDB document
        cursor.execute(
            "INSERT INTO youtube_data (channel_name, Subscribers, Views, Total_videos,Total_likes) VALUES (%s, %s, %s, %s,%s)",
            (document['channel_name'], document['Subscribers'], document['Views'], document['Total_videos'],document['Total_likes'])
        )

    # Commit changes and close connections
    connection.commit()
    cursor.close()
    cursor.close()
    mongo_client.close()



# Streamlit app
st.title("Transfer the data to MongoDB")

# Button to trigger data transfer
if st.button("Transfer Data"):
    st.text("Transferring data...")
    xyz()
    st.text("Data transfer completed!")

st.title("Transfer MongoDB to MySQL")

if st.button("Transfer MongoDB to MySQL"):
    st.text("Transferring data...")
    transfer_data()
    st.text("Data transfer completed!")


# Retrieve Data
# Retrieve all data from a specific column
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'india123',
    'database': 'IITM_youtube_dataharvesting'
}

# Connect to MySQL
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

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



