from datetime import datetime
from config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ImageModel(db.Model):
    __tablename__ = 'images'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(), unique=True, nullable=False)
    text = db.Column(db.Text())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)