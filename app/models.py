import re
import dataclasses 
import json 
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
            seed =  json.loads(seed)
        SeedData(**seed)
        return True
    except Exception as e :
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

    @classmethod #修饰符
    def from_dict(cls, model_dict):
        return cls(**model_dict).save()


class UsersTable(UserMixin, db.Model, BaseModel):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    pubkey = db.Column("pubkey",db.String(64), unique=True)
    comments = db.relationship("CommentsTable", backref="users", lazy="dynamic")

    def __init__(self, **kwargs):
        self.pubkey = "testit"



class SeedsTable(db.Model, BaseModel):
    __tablename__ = "seeds"
    
    group_id = db.Column("group_id",db.String(128), primary_key=True)
    _seed = db.Column("seed", db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    creator = db.Column(db.String(128), db.ForeignKey("users.pubkey"))
    comments = db.relationship("CommentsTable", backref="seeds", lazy="dynamic")

    def __init__(self, seed=None, creator=None, created_at=None):
        if type(seed) == str:
            seed = json.loads(seed)
        self.group_id = seed['group_id']
        self.seed = seed or {}
        self.creator = creator or "unpubkey"
        self.created_at = created_at or datetime.utcnow()

    def __repr__(self):
        return f"<Rum Seed: {self.seed}>"

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, seed):
        #seed: 采用 dataclass 来检查字段来判断是否种子
        if not check_seed(seed):
            raise ValueError(f" not a valid seed \n{seed}\n")
        self._seed = seed

    seed = synonym("_seed", descriptor=seed)

    @property
    def comments_url(self):
        url = None
        kwargs = dict(group_id=self.group_id, _external=True)
        return url_for("api.get_seed_comments", **kwargs)

    def to_dict(self):
        return {
            "seed": self.seed,
            "creator": self.creator,
            "created_at": self.created_at,
            "comment_count": self.comment_count,
            "comments":self.comments_url
        }

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
