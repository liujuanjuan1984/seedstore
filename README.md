# Seed Store

a simple SeedStore template  web application for quorum system.

If you prefer to run it directly on your local machine, I suggest using
[venv](https://docs.python.org/3/library/venv.html).

    pip install -r requirements.txt
    set FLASK_APP=seedstore.py
    flask run

To add some 'test' data you can run

    flask fill-db

Now you can browse the web: 

<http://localhost:5000>

<http://localhost:5000/api/seeds>

<http://localhost:5000/seeds>

Click around, there is not too much.
