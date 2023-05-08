# Made by Enomiis on Github

import requests,json,youtube_dl,urllib
from googleapiclient.discovery import build

# Note that you need to setup a Spotify App in the developper console
# setup is not automatic, you will need to refresh the token when 1 hour passed after your original token

def get_token(): 
    query = "https://accounts.spotify.com/api/token"
    response = requests.post(query,
        
        data={"grant_type": "refresh_token","refresh_token": 'your token'},
        
        headers={"Authorization": "Basic " + "your client thing"}
        )
    
    response_json = response.json()
    print(response_json["access_token"])
    return response_json["access_token"]

api_key = 'your_API_key' # Google API Key
search_token = get_token() # search token to find track on Spotify
print(search_token)
spotify_url = 'https://api.spotify.com/v1/users/your_user/playlists'
add_token = '' # add item to playlist token
spotify_playlist_id = 'your_spotify_playlist_id'
playlist_id = 'your_youtube_playlist_id'
all_song_info = {}  # nested dictionary for all song information

youtube = build('youtube','v3',developerKey=api_key)

def get_spotify_uri(video_title):
    query =f"https://api.spotify.com/v1/search?q={video_title}&type=track&limit=1"
    response = requests.get(query,headers={
        "Content-Type":"application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {search_token}"

    })
    print(response)
    response_json = response.json()
    print(response_json)
    songs = response_json["tracks"]["items"]
    print(songs)
    # only use the first song
    uri = songs[0]["uri"]
    return uri

def youtube_initiate():
    nextPageToken = None
    while True:
        pl_request = youtube.playlistItems().list(
            part='content Details',playlistId=playlist_id,maxResults=50,pageToken=nextPageToken
        )
        pl_response = pl_request.execute()
        nextPageToken =pl_response.get('nextPageToken')
        vid_ids = []
        # to iterate over every video in the playlist and get the ID.
        for item in pl_response['items']:
            vid_ids.append(item['contentDetails']['videoId'])
        vid_request = youtube.videos().list(
            part="snippet",id=",".join(vid_ids)
        )
        vid_response = vid_request.execute()
        # save video title, youtube URL
        for item in vid_response["items"]:
            video_title = item["snippet"]["title"]
            print (video_title)
            youtube_url = "https://www.youtube.com/watch?v={}".format(item["id"])
            # use youtube_dl to collect the song_name and artist name
            video = youtube_dl.YoutubeDL({}).extract_info(youtube_url,download=False)
            try:
                # extract the track name, artist and the spotify uri and save them in our dict
                song_name = video["title"]
                print(song_name)
                spotify_uri = get_spotify_uri(song_name)
                # song information is added if exists
                if(spotify_uri!='null'):
                    all_song_info[video_title] = {"youtube_url": youtube_url, "song_name": song_name, "spotify_uri": spotify_uri}
            except KeyError as e:
                print("Current song details are unavailable ")
        if not nextPageToken:
            break
    print(len(all_song_info))
    print(all_song_info)
    return all_song_info

def add_song_to_playlist(all_song_info):
    uris = [info["spotify_uri"] for song, info in all_song_info.items()]
    request_body=json.dumps({
        "uris":uris
    })
    request_data = json.dumps(uris)
    print(request_data)
    query = f"https://api.spotify.com/v1/playlists/{spotify_playlist_id}/tracks"
    response = requests.post(query,data=request_body,headers = {
        "Content-Type": "application/json","Authorization": f"Bearer {search_token}"
    })
    print(response.status_code)
    response_json=response.json()
    print(response_json)
    return response_json

all_song_info = youtube_initiate()
add_song_to_playlist(all_song_info)