import datetime
import jwt

from app import db, app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_superuser = db.Column(db.Boolean, default=False)
    is_authenticated = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def encode_auth_token(self):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat': datetime.datetime.utcnow(),
            'sub': self.id
        }

        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        ), payload['exp'].isoformat()


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    director = db.Column(db.String(255), nullable=False)
    popularity = db.Column(db.Float)
    imdb_score = db.Column(db.Float)

    genre = db.relationship('Genre', secondary='movie_genre')

    def __repr__(self):
        return '<Movie %r>' % self.name


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    movie = db.relationship('Movie', secondary='movie_genre')

    def __repr__(self):
        return '<Genre %r>' % self.name


class MovieGenre(db.Model):
    __tablename__ = 'movie_genre'

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True)


def populate_db():
    import json

    with open("sample_data/imdb.json", "r") as f:
        data = json.loads(f.read())
        f.close()

    for movie in data:
        m = Movie()
        m.name = movie['name']
        m.director = movie['director']
        m.imdb_score = movie['imdb_score']
        m.popularity = movie['99popularity']

        for genre in movie['genre']:
            genre = genre.strip()
            g = db.session.query(Genre).filter_by(name=genre).one_or_none()

            if not g:
                g = Genre()
                g.name = genre
                db.session.add(g)
                db.session.commit()

            m.genre.append(g)

        db.session.add(m)
        db.session.commit()
