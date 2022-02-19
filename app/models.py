import re
import dataclasses
import json
import time
from datetime import datetime

from flask import url_for
from flask_login import UserMixin
from sqlalchemy.orm import synonym
from werkzeug.security import check_password_hash, generate_password_hash

from app import db

EMAIL_REGEX = re.compile(r"^\S+@\S+\.\S+$")
USERNAME_REGEX = re.compile(r"^\S+$")


@dataclasses.dataclass
class Block:
    BlockId: str
    GroupId: str
    ProducerPubKey: str
    Hash: str
    Signature: str
    TimeStamp: str


@dataclasses.dataclass
class SeedData:
    genesis_block: Block.__dict__
    group_id: str
    group_name: str
    consensus_type: str
    encryption_type: str
    cipher_key: str
    app_key: str
    signature: str
    owner_pubkey: str


def check_seed(seed):
    try:
        if type(seed) == str:
            seed = json.loads(seed)
        SeedData(**seed)
        return True
    except Exception as e:
        print(e)
        return False


def check_length(attribute, length):
    """Checks the attribute's length."""
    try:
        return bool(attribute) and len(attribute) <= length
    except:
        return False


class BaseModel:
    """Base for all models, providing save, delete and from_dict methods."""

    def __commit(self):
        """Commits the current db.session, does rollback on failure."""
        from sqlalchemy.exc import IntegrityError

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def delete(self):
        """Deletes this model from the db (through db.session)"""
        db.session.delete(self)
        self.__commit()

    def save(self):
        """Adds this model to the db (through db.session)"""
        db.session.add(self)
        self.__commit()
        return self

    @classmethod  # 修饰符
    def from_dict(cls, model_dict):
        return cls(**model_dict).save()


class UsersTable(UserMixin, db.Model, BaseModel):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    pubkey = db.Column("pubkey", db.String(64), unique=True)
    comments = db.relationship("CommentsTable", backref="users", lazy="dynamic")

    def __init__(self, **kwargs):
        self.pubkey = "testit"


class SeedsTable(db.Model, BaseModel):
    __tablename__ = "seeds"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.String, unique=True, index=True)
    group_name = db.Column(db.String)
    owner_pubkey = db.Column(db.String)
    consensus_type = db.Column(db.String)
    encryption_type = db.Column(db.String)
    cipher_key = db.Column(db.String)
    app_key = db.Column(db.String)
    signature = db.Column(db.String)
    genesis_block = db.Column(db.String)
    create_at = db.Column(db.Integer)
    add_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    _seed = db.Column("seed", db.JSON)
    creator = db.Column(db.String(128), db.ForeignKey("users.pubkey"))
    comments = db.relationship("CommentsTable", backref="seeds", lazy="dynamic")

    def __init__(self, **seed):
        if "owner_encryptpubkey" in seed:
            del seed["owner_encryptpubkey"]

        super().__init__(**seed)
        self.genesis_block = str(seed["genesis_block"])
        self.create_at = int(seed["genesis_block"]["TimeStamp"])
        self._seed = seed

    def __repl__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {
            "genesis_block": eval(self.genesis_block),
            "group_id": self.group_id,
            "group_name": self.group_name,
            "owner_pubkey": self.owner_pubkey,
            "consensus_type": self.consensus_type,
            "encryption_type": self.encryption_type,
            "cipher_key": self.cipher_key,
            "app_key": self.app_key,
            "signature": self.signature,
        }

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, seed):
        # seed: 采用 dataclass 来检查字段来判断是否种子
        if not check_seed(seed):
            flash("not a seed.")
            raise ValueError(f" not a valid seed \n{seed}\n")
        self._seed = seed

    seed = synonym("_seed", descriptor=seed)

    @property
    def comments_url(self):
        url = None
        kwargs = dict(group_id=self.group_id, _external=True)
        return url_for("api.get_seed_comments", **kwargs)

    @property
    def comment_count(self):
        return self.comments.order_by(None).count()


class CommentsTable(db.Model, BaseModel):
    """用户对种子网络的评价"""

    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    commenttext = db.Column(db.String(512))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    stars = db.Column(db.Integer)
    creator = db.Column(db.String(64), db.ForeignKey("users.pubkey"))
    group_id = db.Column(db.Integer, db.ForeignKey("seeds.group_id"))

    def __init__(self, commenttext, stars, group_id, creator=None, created_at=None):
        self.commenttext = commenttext
        self.group_id = group_id
        self.stars = stars
        self.creator = creator
        self.created_at = created_at or datetime.utcnow()

    def __repr__(self):
        return "<{} 评价: {} by {}>".format(
            self.group_id, self.commenttext, self.creator or "None"
        )

    def to_dict(self):
        return {
            "commenttext": self.commenttext,
            "creator": self.creator,
            "created_at": self.created_at,
            "stars": self.stars,
            "group_id": self.group_id,
        }
