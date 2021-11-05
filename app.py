from flask import Flask, render_template
import os, json, random, requests

# Configuration
 
app = Flask(__name__)

# Functions

def get_dict_from_json(json_file):
    fjson = open(json_file, 'r')
    song_dict = json.loads(fjson.read())
    return song_dict


# Routes 

@app.route('/')
def root():
    return render_template('home.html')

@app.route('/display-song', methods=['POST'])
def display_song():
    
    song_api_url = 'https://api-mashup-neesjo.herokuapp.com/api/recommendation'
    song_rec_data = {"seed_genres":"pop,rock,jazz"}
    response = requests.post(song_api_url, data=song_rec_data)
    return response.text


    #return render_template('display_song.html', keys = song_info_keys, data = this_song_dict[index])

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    
    app.run(port=port, debug=True) 