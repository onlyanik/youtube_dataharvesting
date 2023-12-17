from googleapiclient.discovery import build
import streamlit as st
import pandas as pd
import seaborn as sns
import pymongo

def xyz():

    #Connecting MongoDB by pymongo

    client = pymongo.MongoClient("mongodb://localhost:27017")
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
    db = client['IITM_youtube_dataharvesting']
    collection = db['Capstone_youtubedata']

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
        collection.insert_one(x)


    # the output obtained in json format


# Streamlit app
st.title("Transfer the data to MongoDB")

# Button to trigger data transfer
if st.button("Transfer Data"):
    st.text("Transferring data...")
    xyz()
    st.text("Data transfer completed!")

 
