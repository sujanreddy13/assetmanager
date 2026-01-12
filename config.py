from datetime import timedelta

class Config:
    SECRET_KEY = "mysecretkey"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:Sribalaji%4013@localhost:5432/asset_manager"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    