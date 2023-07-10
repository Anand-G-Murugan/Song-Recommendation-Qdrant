# Song-Recommendation-Qdrant

## Quickstart
* Clone this repo into a directory of your choice.
* Install Qdrant via Docker. (refer:https://qdrant.tech/documentation/quick-start/)
* Note: The commands are shown in UNIX-shell, refer `qdrant_commands_for_windows.txt` for the windows alternatives.
* The ipynb notebook is for demonstration purposes.
* For the actual app, navigate to the directory in your terminal and run `streamlit run song_rec_streamlit.py`.

# Project Description
* This is an implementation of a recommendation engine using the Qdrant Recommendation API.
* We source the data from https://www.kaggle.com/datasets/geomack/spotifyclassification. (Note: You can get your own data using the spotify API).
* The data is vectorized and stored in a Qdrant collection.
* The Recommendation API takes positive and negative feedback from the user as well as artist filters and uses vector similarity to assign a score to each of the songs in our data.
* The top 5 songs are displayed back to the user. 
