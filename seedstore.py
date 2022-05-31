from app import create_app

app = create_app("development")


@app.cli.command()
def test():
    """Runs the unit tests."""
    import sys
    import unittest

    tests = unittest.TestLoader().discover("tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.errors or result.failures:
        sys.exit(1)


@app.cli.command()
def fill_db():

    from utils.fake_generator import FakeGenerator

    FakeGenerator().start()  # side effect: deletes existing data


@app.cli.command()
def update_db():
    from officy import JsonFile

    from config import Config
    from utils.data_update import SeedsInit

    seeds = JsonFile(Config.SeedsDataFile).read()
    SeedsInit().start(seeds)
