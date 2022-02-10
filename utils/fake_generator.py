import random
from datetime import datetime

import forgery_py

from app import db
from app.models import CommentsTable, SeedsTable, UsersTable


class FakeGenerator:
    def __init__(self):
        # in case the tables haven't been created already
        db.drop_all()
        db.create_all()

    def generate_fake_date(self):
        return datetime.combine(forgery_py.date.date(True), datetime.utcnow().time())

    def generate_fake_users(self, count):
        for _ in range(count):
            UsersTable(
                pubkey=forgery_py.internet.user_name(True),
            ).save()

    def generate_fake_seeds(self, count):
        # for the creator relation we need users
        for _ in range(count):
            SeedsTable(
                seed={
                    "genesis_block": {
                        "BlockId": "eba2a180-473e-46fc-80e2-8ef1fab85f10",
                        "GroupId": "e7ca1441-449a-497a-a458-dcc6631c1bd9",
                        "ProducerPubKey": "CAISIQKQTRT79u3hUFSy4Xb0yFt2ZRmv03ln8bm0IwkuNotNdw==",
                        "Hash": "M/dxRWOJY4CERDT9+1LnHZRGVfEeFz4ODppYZ5ytsjM=",
                        "Signature": "MEUCIHkzvphNEEAuZ1+Zlk89IgvzDOE62ylnhQK0IYIpMFJSAiEA1lOH5ItoyxGl5xzJejigMBzvICz+0PHCFWVzYZiJ/k4=",
                        "TimeStamp": "1643186113157303700"
                    },
                    "group_id": "e7ca1441-449a-497a-a458-dcc6631c1bd9",
                    "group_name": "2022断舍离",
                    "owner_pubkey": "CAISIQKQTRT79u3hUFSy4Xb0yFt2ZRmv03ln8bm0IwkuNotNdw==",
                    "consensus_type": "poa",
                    "encryption_type": "public",
                    "cipher_key": "17cdeb65d678d5406f13665ab91cb5f545846f0a4413fc6da70c89b928579103",
                    "app_key": "group_timeline",
                    "signature": "30450220207b2305ade56bee9e94b9c5530d27f4df5958a0aa7a0dcdb1f3c29e043cd795022100a5e368044746e726d77715a1b944ff35411a53016d508c5576d3dbb57486b257"
                    },
                creator="faker",
                created_at=self.generate_fake_date(),
            ).save()

    def generate_fake_todo(self, count):
        seeds = SeedsTable.query.all()
        for _ in range(count):
            seed = random.choice(seeds)
            comment = CommentsTable(
                commenttext=forgery_py.forgery.lorem_ipsum.words(),
                stars=random.choice(list(range(1,6))),
                group_id=seed.group_id,
                creator=seed.creator,
                created_at=self.generate_fake_date(),
            ).save()


    def generate_fake_data(self, count):
        # generation must follow this order, as each builds on the previous
        self.generate_fake_users(count)
        self.generate_fake_seeds(count * 3)
        self.generate_fake_todo(count * 6)

    def start(self, count=2):
        self.generate_fake_data(count)
