server is setup: http://127.0.0.1:8000

next:
Step 3 — Set up PostgreSQL and connect Flask to it


flask migrate setup:
initializes db migration: python -m flask --app run db init 
creates migration model based on song model(It only creates the migration instructions): python -m flask --app run db migrate -m "create songs table"
creates table in the postgresql: python -m flask --app run db upgrade

migrate = prepare the database change
upgrade = execute the database change

Song model
   ↓
db migrate
   ↓
migration file created
   ↓
db upgrade
   ↓
PostgreSQL database actually changes
