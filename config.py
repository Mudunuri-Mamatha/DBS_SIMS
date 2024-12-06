import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/sims_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
