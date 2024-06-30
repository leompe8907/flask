import os
class Config:
  SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/blogdb'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SECRET_KEY = os.urandom(24)