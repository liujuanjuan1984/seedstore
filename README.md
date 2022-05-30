# Seed Store

A simple SeedStore template web application for quorum system.

If you prefer to run it directly on your local machine, I suggest using
[venv](https://docs.python.org/3/library/venv.html).

```sh
pip install -r requirements.txt
set FLASK_APP=seedstore.py
flask run
```

Format:

```bash
isort .
black -l 80 -t py37 -t py38 -t py39 -t py310 .
black -l 120 -t py37 -t py38 -t py39 -t py310 .

```

To add some 'test' data you can run:

```sh
flask fill-db
```

To add more seeds data from jsonfile:

```sh
flask update-db
```

Now you can browse the web:

- <http://localhost:5000>
- <http://localhost:5000/api/seeds>
- <http://localhost:5000/seeds>

Click around, there is not too much.
