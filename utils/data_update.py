from officy import JsonFile

from app import db
from app.models import SeedsTable


class SeedsInit:
    def __init__(self):
        db.drop_all()
        db.create_all()

    def update_seed(self, seeds):
        failed = []
        for group_id in seeds:
            try:
                SeedsTable(**seeds[group_id], creator="history.data").save()
            except Exception as e:
                print(group_id, e)

    def start(self, seeds):
        self.update_seed(seeds)
