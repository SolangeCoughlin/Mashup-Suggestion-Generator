from flask import Flask, render_template, request
import os, json, random, requests

# Configuration
 
app = Flask(__name__)

# Functions

def get_dict_from_json(json_file):
    fjson = open(json_file, 'r')
    song_dict = json.loads(fjson.read())
    return song_dict

# Receives one track dict object and returns the artist as a string
def get_artist(track_dict):
    artist = track_dict["artists"][0]["name"]
    return artist

def get_title(track_dict):
    title = track_dict["name"]
    return title

# Routes 

@app.route('/')
def root():
    return render_template('home.html')

@app.route('/display-song', methods=['POST'])
def display_song():

    song_api_url = 'https://api-mashup-neesjo.herokuapp.com/api/recommendation'
    
    # Get criteria values from form on the home page and format the genre seed into the format required
    criteria = request.form
    genre = f'{criteria["seed_genre1"]},{criteria["seed_genre2"]},{criteria["seed_genre3"]}'
    song_rec_data = {"seed_genres":genre}
    
    # Add only items that have been filled out by the user to the data object holding values for microservice call
    for item in criteria:
        if criteria[item] != "none" and item != "seed_genres":
            song_rec_data[item] = criteria[item]

    # Make a call to the microservice using data supplied by the user and get the microservice response as a json
    response = requests.post(song_api_url, data=song_rec_data)
    response = response.json()

    # Render information for one of the songs on the page
    suggestions = {}
    for track in response:
        print("track is " + track)
        this_track = response[track]
        song_dict = {"Artist": get_artist(this_track), "Title": get_title(this_track)}
        song_dict_keys = song_dict.keys()
        suggestions[track] = song_dict
    return render_template('display_song.html', keys = song_dict_keys, data = suggestions)

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    
    app.run(port=port, debug=True) 