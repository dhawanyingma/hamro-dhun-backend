from app import app, db
from flask import request
from sqlalchemy import text
from app.models.songs import Song

@app.route("/")
def home():
    return {"message":"Your flask app is running"}

@app.route("/songs", methods= ["POST"])
def create_song():
    data = request.get_json()
    if not data:
        return {"error": "Request Body is requested"}, 400

    if not data.get("title") or not data.get("artist") or not data.get("lyrics"):
        return {"error": "title, artist, and lyrics are requested"}, 400

    song = Song(
        title=data["title"],
        artist=data["artist"],
        lyrics=data["lyrics"],
        chords=data.get("chords")
    )  
    db.session.add(song)
    db.session.commit()
    return {
            "message" : "Song created successfully",
            "song":{
                "id" : song.id,
                "title" : song.title,
                "artist" : song.artist,
                "chords" : song.chords
            }
        },201
    
@app.route("/songs", methods=["GET"])
def get_songs():
    songs = db.session.scalars(db.select(Song).order_by(Song.id)).all()
    result = []

    for song in songs:
        result.append(
            {
                "id" : song.id,
                "artist":song.artist,
                "title":song.title,
                "lyrics":song.lyrics,
                "chords":song.chords
            }
        )
    return result, 200

@app.route("/songs/<int:id>", methods=["GET"])
def get_song_by_id(id):
    song = db.session.get(Song, id)

    if not song:
        return {
            "message": "The song with the given ID does not exist. Please try again."
        }, 404

    requested_song = {
        "id": song.id,
        "artist": song.artist,
        "title": song.title,
        "lyrics": song.lyrics,
        "chords": song.chords
    }
    return requested_song, 200

@app.route("/songs/<int:id>", methods=["PATCH"])
def song_update(id):
    song = db.session.get(Song, id)
    if not song:
        return {
            "message": "The song with the given ID does not exist. Please try again."
        }, 404
    data = request.get_json()
    if not data:
        return {
            "message" : "Request body is required"
        }, 400

    if "title" in data:
        song.title = data["title"]
    if "artist" in data:
        song.artist = data["artist"]
    if "lyrics" in data:
        song.lyrics = data["lyrics"]
    if "chords" in data:
        song.chords = data["chords"]
    db.session.commit()

    return {
        "message" : "The song details updated successfully.",
        "song" : {
            "title" : song.title,
            "artist" : song.artist,
            "lyrics" : song.lyrics,
            "chords" : song.chords
        }
    }, 200

@app.route("/songs/<int:id>", methods = ["DELETE"])
def delete_song(id):
    song = db.session.get(Song, id)
    if not song:
        return { 
            "message" : "Song not found"
        }, 404

    db.session.delete(song)
    db.session.commit()
    return {
        "message" : "Song has been deleted successfully."
    }, 200
    

    

@app.route("/test_db")
def test_db():
    db.session.execute(text("select 1"))
    return {"message" : "DB connection successful"}