import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'postgresql://myuser:mypassword@db:5432/mydatabase'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ConfigP:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'postgresql://myuserp:mypasswordp@dbp:5433/mydatabasep'
    SQLALCHEMY_TRACK_MODIFICATIONS = False