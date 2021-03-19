# imdb
imdb movie APIs

Project built with flask and postgresql

Run flask app

```
flask run
```

Create db tables and populate tables

```
flask shell

> from app import db
> import models
> db.create_all()
> models.populate_db()
```

Please find API documentation in `IMDB Task - doc.pdf`