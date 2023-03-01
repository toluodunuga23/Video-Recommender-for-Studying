# What is pushed to github

import os
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from textblob import TextBlob


# Set the API key
API_KEY = "{{ Enter Your API_KEY}}}"

# Authenticate with the YouTube API
credentials = service_account.Credentials.from_service_account_file(
    '/enter File Path name of .json', scopes=['https://www.googleapis.com/auth/youtube.force-ssl']
)

youtube = build('youtube', 'v3', credentials=credentials)

# Define a function to search for videos based on a query
def search_videos(query):
    request = youtube.search().list(
        part='id,snippet',
        type='video',
        q=query,
        maxResults=10,
        fields='items(id(videoId),snippet(title,description,thumbnails(default(url))))'
    )
    response = request.execute()
    return response['items']

# Define a function to get the comments of a video
def get_comments(video_id):
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText'
    )
    response = request.execute()
    comments = []
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)
    return comments

# Define the Streamlit app
def app():
    # Page title
    st.title('YouTube Video Recommender')

    # User input for topic of study
    topic = st.text_input('What topic are you studying?', 'i.e Python programming')

    # Search for videos based on topic
    videos = search_videos(topic)
   

    # Display video recommendations sorted by sentiment of comments
    st.subheader('Video Recommendations')
    video_sentiments = []
    for video in videos:
        st.write(video['snippet']['title'])
        st.write(video['snippet']['description'])
    
        st.video(f"https://www.youtube.com/watch?v={video['id']['videoId']}")
        
        # Get comments of video and calculate average sentiment
        comments = get_comments(video['id']['videoId'])
        comment_sentiments = [TextBlob(comment).sentiment.polarity for comment in comments]
        average_sentiment = sum(comment_sentiments) / len(comment_sentiments)
        video_sentiments.append((video, average_sentiment))
        

    # Sort videos by sentiment and display in order
    video_sentiments = sorted(video_sentiments, key=lambda x: x[1], reverse=True)
    for video, sentiment in video_sentiments:
        st.write(video['snippet']['title'])
        st.write(video['snippet']['description'])
        st.video(f"https://www.youtube.com/watch?v={video['id']['videoId']}")
        st.write('Sentiment:', sentiment)
        print('Sentiment:', sentiment)

if __name__ == '__main__':
    app()
