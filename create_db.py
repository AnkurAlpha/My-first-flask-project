# just an extra piece written to create the database
# just execute it to create an initial database
from app import app, db

with app.app_context():
    db.create_all()
    print("Database tables created.")
