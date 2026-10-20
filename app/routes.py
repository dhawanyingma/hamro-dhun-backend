from app import app, db
from flask import jsonify, request
from sqlalchemy import or_, text,select
from app.models.songs import Song

@app.route("/")
def home():
    """
    Check that the API is responding.
    ---
    tags:
      - General
    responses:
      200:
        description: API is responding.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Your flask app is running
    """
    return {"message":"Your flask app is running"}

@app.route("/songs", methods= ["POST"])
def create_song():
    """
    Create a song.
    ---
    tags:
      - Songs
    parameters:
      - name: song
        in: body
        required: true
        schema:
          type: object
          required:
            - title
            - artist
            - lyrics
          properties:
            title:
              type: string
              example: Example Song
            artist:
              type: string
              example: Example Artist
            lyrics:
              type: string
              example: Example lyrics
            chords:
              type: string
              example: C G Am F
    responses:
      201:
        description: Song created successfully.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Song created successfully
            song:
              type: object
              properties:
                id:
                  type: integer
                title:
                  type: string
                artist:
                  type: string
                chords:
                  type: string
      400:
        description: Request body or required song fields are missing.
    """

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

    """
    Get all songs.
    ---
    tags:
      - Songs
    responses:
      200:
        description: List of songs.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              artist:
                type: string
              lyrics:
                type: string
              chords:
                type: string
    """

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


@app.get("/songs/search")
def search_songs():
    """
    Search songs by title, artist, or lyrics.
    ---
    tags:
      - Songs
    parameters:
      - name: q
        in: query
        type: string
        required: true
        description: Text to search for.
    responses:
      200:
        description: Matching songs, or an empty list if there are no matches.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              artist:
                type: string
              lyrics:
                type: string
              chords:
                type: string
      400:
        description: The q query parameter is missing or blank.
    """

    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"message": "Please provide a search term in q"}), 400

    sort_by = request.args.get("sort", "").strip().lower()



    stmt = (select(Song)
            .where(
                or_(
                    Song.title.ilike(f"%{q}%"),
                    Song.artist.ilike(f"%{q}%"),
                    Song.lyrics.ilike(f"%{q}%")
                )
            )
            .order_by(Song.title.asc())
            )
    
    results = db.session.execute(stmt)
    songs = results.scalars().all()

    song_list=[]
    for song in songs:
        song_list.append({
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "lyrics": song.lyrics,
            "chords": song.chords
        })
    return jsonify(song_list), 200


@app.route("/songs/<int:id>", methods=["GET"])
def get_song_by_id(id):
    """
    Get a song by its ID.
    ---
    tags:
      - Songs
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the song to retrieve.
    responses:
      200:
        description: The requested song.
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            artist:
              type: string
            lyrics:
              type: string
            chords:
              type: string
      404:
        description: Song with that ID was not found.
    """

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
    return jsonify(requested_song), 200

@app.route("/songs/<int:id>", methods=["PATCH"])
def song_update(id):

    """
    Update a song.
    ---
    tags:
      - Songs
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the song to update.
      - name: song
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: Updated Song Title
            artist:
              type: string
              example: Updated Artist
            lyrics:
              type: string
              example: Updated lyrics
            chords:
              type: string
              example: D A Bm G
    responses:
      200:
        description: Song details updated successfully.
        schema:
          type: object
          properties:
            message:
              type: string
            song:
              type: object
              properties:
                title:
                  type: string
                artist:
                  type: string
                lyrics:
                  type: string
                chords:
                  type: string
      400:
        description: Request body is missing.
      404:
        description: Song with that ID was not found.
    """

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

    """
    Delete a song.
    ---
    tags:
      - Songs
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the song to delete.
    responses:
      200:
        description: Song was deleted successfully.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Song has been deleted successfully.
      404:
        description: Song with that ID was not found.
    """
    
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