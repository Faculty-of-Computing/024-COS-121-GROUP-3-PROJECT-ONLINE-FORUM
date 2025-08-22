from app import app, db
from app.models import User, Topic, Reply

with app.app_context():
    db.drop_all()  # This will drop all tables
    db.create_all() # This will create all tables from scratch
    print("Database tables recreated successfully!")
