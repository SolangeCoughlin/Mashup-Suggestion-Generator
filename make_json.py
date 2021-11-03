import json

song_dict = {"songs":[
    {
        "title": "Grail",
        "artist": "Tripp St",
        "bpm": "120",
        "key": "C",
        "danceability": "4"
    },
    {
        "title": "Down",
        "artist": "Oh Wonder",
        "bpm": "65",
        "key": "D",
        "danceability": "1"
    },
    {
        "title": "Take Me To The Riot",
        "artist": "Stars",
        "bpm": "92",
        "key": "F",
        "danceability": "6"
    },
    {
        "title": "Radar Detector",
        "artist": "Darwin Deez",
        "bpm": "100",
        "key": "C",
        "danceability": "9"
    }
    ]
    }

def make_song_json(song_dict):
    song_json = json.dumps(song_dict)
    with open('song_dict.json', 'w') as outfile:
        outfile.write(song_json)


def main():
    make_song_json(song_dict)

if __name__ == '__main__':
    main()