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

# Receives form object, and formats it into a dict that can be passed to microservice API. Returns this dict.
# The dict contains a dict for track 1, and a dict for track 2
def format_criteria_obj(criteria):
    
    song_rec_data = {}

    genre = f'{criteria["seed_genre1"]},{criteria["seed_genre2"]},{criteria["seed_genre3"]}'
    song_rec_data["track_1"] = {"seed_genres": genre}

    # There will be no track 2 if table isn't filled out
    if "2_seed_genre1" in criteria and criteria["2_seed_genre1"] != "none":
        genre = f'{criteria["2_seed_genre1"]},{criteria["2_seed_genre2"]},{criteria["2_seed_genre3"]}'
        song_rec_data["track_2"] = {"seed_genres": genre}
        
    # Add only items that have been filled out by the user to the data object holding values for microservice call
    for item in criteria:
        if criteria[item] != "none" and "seed_genre" not in item and "2_" not in item:
            song_rec_data["track_1"][item] = criteria[item]
        if criteria[item] != "none" and "seed_genre" not in item and "2_" in item:
            song_rec_data["track_2"][item] = criteria[item]

    return song_rec_data

# Receives a dict containing the form data the user entered, already formatted for the microservice, and returns a response from the microservice
# in json format.
def make_spotify_call(song_rec_data):
    song_api_url = 'https://api-mashup-neesjo.herokuapp.com/api/recommendation'
    response = requests.post(song_api_url, data=song_rec_data)
    
    return response.json()

# Receives a response in json format and returns a dict containing the Artist and Title of the two songs suggested.
def format_suggestions(response):
    suggestions = {}
    for track in response:
        this_track = response[track]
        song_dict = {"Artist": get_artist(this_track), "Title": get_title(this_track)}
        suggestions[track] = song_dict

    return suggestions

# Checks if the input to the form is valid. If it returns True, there is invalid input.
def input_error(criteria):

    result = False
    # Raise an error if seed_genre1 for song 1 is empty. Needed to make Spotify call
    if criteria["seed_genre1"] == "none" or criteria["seed_genre2"] == "none" or criteria["seed_genre3"] == "none":
        result = True

    # For both the following error handlers, user's must fill out either all genres, or no genres for Second Song
    if criteria["2_seed_genre1"] == "none" and (criteria["2_seed_genre2"] != "none" or criteria["2_seed_genre3"] != "none"):
        result = True

    if criteria["2_seed_genre1"] != "none" and (criteria["2_seed_genre2"] == "none" or criteria["2_seed_genre3"] == "none"):
        result = True

    return result

# Routes 

@app.route('/')
def root():
    return render_template('home.html')

@app.route('/display-song', methods=['POST'])
def display_song():
    
    # Get criteria values from form on the home page and format the genre seed into the format required
    criteria = request.form

    if input_error(criteria):
        error_message="Make sure at least First Song has all three genres filled out"
        return render_template('home.html', error_message = error_message)
    
    song_rec_data = format_criteria_obj(criteria)

    # Make a call to the microservice using data supplied by the user and get the microservice response as a json
    song_1_response = make_spotify_call(song_rec_data["track_1"])
    song_2_response = None
    if len(song_rec_data) > 1:
        song_2_response = make_spotify_call(song_rec_data["track_2"])

    # Render information for two songs on the page
    song_suggestions = format_suggestions(song_1_response)
    if song_2_response:
        song_suggestions_2 = format_suggestions(song_2_response)
        song_suggestions["track_2"] = song_suggestions_2["track_1"]
    keys = ["Artist", "Title"]
    
    return render_template('display_song.html', keys = keys, data = song_suggestions)

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    
    app.run(port=port, debug=True) 