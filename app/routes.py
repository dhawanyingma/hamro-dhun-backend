from app import app, db
from sqlalchemy import text

@app.route("/")
def home():
    return {"message":"Your flask app is running"}

@app.route("/test_db")
def test_db():
    db.session.execute(text("select 1"))
    return {"message" : "DB connection successful"}