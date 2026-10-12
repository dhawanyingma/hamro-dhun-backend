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
        return {"error": "Request Body is Required"}, 400

    if not data.get("title") or not data.get("artist") or not data.get("lyrics"):
        return {"error": "title, artist, and lyrics are required"}, 400

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

    

@app.route("/test_db")
def test_db():
    db.session.execute(text("select 1"))
    return {"message" : "DB connection successful"}