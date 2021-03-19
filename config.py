class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:abc123@localhost/imdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "c4llKiB7g-pIUwukcJNgACmTfkVFGmJnzbVxcEY2Hms"
