import streamlit as st
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client import QdrantClient
from sklearn.preprocessing import MinMaxScaler
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct


def makeCollection():
    # Function to initialize the qdrant collection. (This is the code from song_recc.ipynb)
    client = QdrantClient("http://65.1.33.97", port=6333)
    existing_collections = client.get_collections()
    flag = 0
    for i in existing_collections.collections:
        if(i.name=="spotify_collection"):
            flag = 1

    if(flag == 0):
        df = pd.read_csv("./data_folder/data.csv", index_col=0)
        numeric_cols = ['acousticness', 'danceability', 'duration_ms', 'energy',
        'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
        'speechiness', 'tempo', 'time_signature', 'valence']
        non_numeric_cols = ['song_title', 'artist']
        scaler = MinMaxScaler()
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
        points = []
        for row in df.iterrows():
            temp = PointStruct(id = row[0], 
                            vector = list(map(float, row[1][:-2].tolist())),
                            payload={
                                "artist" :  row[1][-1],
                                "song_title" : row[1][-2],
                            }
            )
            points.append(temp)
        client.recreate_collection(
            collection_name="spotify_collection",
            vectors_config = VectorParams(size = 14, distance=models.Distance.COSINE)
        )

        operation_info = client.upsert(
            collection_name="spotify_collection",
            wait=True,
            points = points
        )
    return client






def Recommend(client, positive_ids, negative_ids, artist_whitelist, artist_blacklist):
    # Function to recommend a song based on positive, negative and artist filters.
    
    must = []
    must_not = []

    for artist in artist_blacklist:
        must_not.append(models.FieldCondition(
            key = "artist",
            match = models.MatchValue(value = artist)
            ))
    
    for artist in artist_whitelist:
        must.append(models.FieldCondition(
            key = "artist",
            match = models.MatchValue(value = artist)
            ))


    search_result = client.recommend(
        collection_name="spotify_collection",
        positive=positive_ids,
        negative=negative_ids, 
        query_filter= models.Filter(
            must = must,
            must_not = must_not,
        ),
        # Change this limit if you wanna see more results
        limit = 5
    )
    
    
    artists = []
    songs = []
    for i in search_result:
        artists.append(i.payload['artist'])
        songs.append(i.payload['song_title'])
    data = {'artist': artists, 'song_title': songs}
    df = pd.DataFrame(data)
    return df



    



# Streamlit application
def main():
    
    client = makeCollection()


    st.title("Song Dataframe Application")

    # Load Data
    df = pd.read_csv("data_folder/data.csv")
    last_two_columns = df.iloc[:, -2:]
    st.dataframe(last_two_columns)
    
    # User input fields
    st.subheader("Input IDs")
    positive_ids = st.text_input("Positive IDs (comma-separated)", help="Enter positive song IDs")
    negative_ids = st.text_input("Negative IDs (comma-separated)", help="Enter negative song IDs")
    
    # Whitelist and blacklist
    st.subheader("Input Artist Whitelist and Blacklist (Optional)")
    artist_whitelist = st.text_input("Artist Whitelist (comma-separated, CASE sensitive)", help="Enter artist names to whitelist")
    artist_blacklist = st.text_input("Artist Blacklist (comma-separated, CASE sensitive)", help="Enter artist names to blacklist")
    
    # Submit button
    if st.button("Submit"):
        # Convert input strings to lists
        positive_ids = [int(id.strip()) for id in positive_ids.split(",") if id.strip()]
        negative_ids = [int(id.strip()) for id in negative_ids.split(",") if id.strip()]
        artist_whitelist = [artist.strip() for artist in artist_whitelist.split(",") if artist.strip()]
        artist_blacklist = [artist.strip() for artist in artist_blacklist.split(",") if artist.strip()]
        
        # Call Recommend() function with provided inputs
        results_df = Recommend(client, positive_ids, negative_ids, artist_whitelist, artist_blacklist)
        
        # Display the dataframe
        # Replace the following code with your own dataframe creation and display logic
        
        st.dataframe(results_df)


if __name__ == "__main__":
    main()
