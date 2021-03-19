from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

import os
import config
from decorators import admin_login_required


app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

import models


@app.route('/movies', methods=['GET'])
def list_movies():
    results = {"objects": []}
    search_query = request.args.get('search')

    if search_query:
        movies = models.Movie.query\
            .filter(models.Movie.name.startswith(search_query)).all()
    else:
        movies = db.session.query(models.Movie).all()

    for m in movies:
        d = {}
        d['name'] = m.name
        d['director'] = m.director
        d['imdb_score'] = m.imdb_score
        d['99popularity'] = m.popularity
        d['genre'] = [g.name for g in m.genre]
        d['id'] = m.id

        results['objects'].append(d)

    return jsonify(results)


@app.route('/movies/add', methods=['POST'])
@admin_login_required
def add_movie():
    body = request.get_json(force=True)

    m = models.Movie()
    m.name = body['name']
    m.director = body['director']
    m.popularity = body['99popularity']
    m.imdb_score = body['imdb_score']

    for genre in body['genre']:
        genre = genre.strip()
        genre_obj = db.session.query(models.Genre).filter_by(name=genre).one_or_none()

        if not genre_obj:
            genre_obj = models.Genre()
            genre_obj.name = genre
            db.session.add(genre_obj)
            db.session.commit()

        m.genre.append(genre_obj)

    db.session.add(m)
    db.session.commit()

    return jsonify({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/movies/remove/<id>', methods=['DELETE'])
@admin_login_required
def remove_movie(id):
    m = models.Movie.query.filter_by(id=id).first()

    res = {
        "success": True
    }
    res_type = {'ContentType':'application/json'}

    if not m:
        res['message'] = 'movie doesn\'t exist'

        return jsonify(res), 301, res_type

    m.genre = []
    db.session.add(m)
    db.session.commit()

    models.Movie.query.filter_by(id=id).delete()
    db.session.commit()

    return jsonify(res), 200, res_type


@app.route('/movies/edit/<id>', methods=['PATCH'])
@admin_login_required
def edit_movie(id):
    m = models.Movie.query.filter_by(id=id).first()

    res = {
        "success": True
    }
    res_type = {'ContentType':'application/json'}

    if not m:
        res['message'] = 'movie doesn\'t exist'

        return jsonify(res), 301, res_type

    body = request.get_json(force=True)

    if body.get('name'):
        m.name = body.get('name')

    if body.get('director'):
        m.director = body['director']

    if body.get('99popularity') is not None:
        m.popularity = body['99popularity']

    if body.get('imdb_score') is not None:
        m.imdb_score = body['imdb_score']

    db.session.add(m)
    db.session.commit()

    return jsonify(res), 200, res_type


@app.route('/login', methods=['POST'])
def login():
    body = request.get_json(force=True)
    username = body['username']
    pwd = body['password']

    user = models.User.query.filter_by(username=username).first()

    res = {
        "success": True
    }
    res_type = {'ContentType':'application/json'}

    if not user:
        res['success'] = False
        res['message'] = 'User not found'

        return jsonify(res), 401, res_type

    elif bcrypt.check_password_hash(bcrypt.generate_password_hash(pwd),
                                    user.password):
        res['success'] = False
        res['message'] = 'Wrong password'

        return jsonify(res), 401, res_type

    user.is_authenticated = True
    db.session.add(user)
    db.session.commit()
    res['token'], res['token_expiry'] = user.encode_auth_token()

    return jsonify(res), 200, res_type


if __name__ == '__main__':
    app.run()