import os

class Config(object):
    SECRET_KEY = 'your_secret_key'
    UPLOAD_FOLDER = '/path/to/uploads/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/Photo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False