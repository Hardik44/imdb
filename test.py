import requests
import json


def admin_add_movie():
    body = {
        "username": "david_xavier",
        "password": "imdb@1234"
    }

    login_url = "http://localhost:5000/login"
    add_url = "http://localhost:5000/movies/add"
    res = requests.post(login_url, data=json.dumps(body))
    assert res.status_code == 200

    token = res.json()['token']

    new_movie = {
        "name": "New sample movie 1",
        "director": "New sample director 1",
        "99popularity": 75.5,
        "imdb_score": 9.5,
        "genre": ["Action", "Sci-fi"]
    }
    headers = {"Authorization": token}

    res = requests.post(add_url, data=json.dumps(new_movie), headers=headers)
    assert res.status_code == 200


if __name__ == '__main__':
    admin_add_movie()