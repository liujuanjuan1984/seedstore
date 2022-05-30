from flask import abort, request, url_for

from app.api import api
from app.models import CommentsTable, SeedsTable, UsersTable


@api.route("/")
def get_routes():
    return {
        "users": url_for("api.get_users", _external=True),
        "seeds": url_for("api.get_seeds", _external=True),
    }


@api.route("/users/")
def get_users():
    return {"users": [user.to_dict() for user in UsersTable.query.all()]}


@api.route("/user/<string:pubkey>/")
def get_user(pubkey):
    user = UsersTable.query.filter_by(pubkey=pubkey).first_or_404()
    return user.to_dict()


@api.route("/user/", methods=["POST"])
def add_user():
    try:
        user = UsersTable(
            pubkey=request.json.get("pubkey"),
        ).save()
    except:
        abort(400)
    return user.to_dict(), 201


@api.route("/user/<string:pubkey>/seeds/")
def get_user_seeds(pubkey):
    user = UsersTable.query.filter_by(pubkey=pubkey).first_or_404()
    seeds = user.seeds
    return {"seeds": [seed.to_dict() for seed in seeds]}


@api.route("/user/<string:pubkey>/seed/<group_id>/")
def get_user_seed(pubkey, group_id):
    user = UsersTable.query.filter_by(pubkey=pubkey).first()
    seed = SeedsTable.query.get_or_404(group_id)
    if not user or pubkey != seed.creator:
        abort(404)
    return seed.to_dict()


@api.route("/user/<string:pubkey>/seed/", methods=["POST"])
def add_user_seed(pubkey):
    user = UsersTable.query.filter_by(pubkey=pubkey).first_or_404()
    try:
        seed = SeedsTable(seed=request.json.get("seed"), creator=user.pubkey).save()
    except:
        abort(400)
    return seed.to_dict(), 201


@api.route("/seeds/")
def get_seeds():
    seeds = SeedsTable.query.all()
    return {"seeds": [seed.to_dict() for seed in seeds]}


@api.route("/seed/<group_id>/")
def get_seed(group_id):
    seed = SeedsTable.query.get_or_404(group_id)
    return seed.to_dict()


@api.route("/seed/", methods=["POST"])
def add_seed():
    try:
        seed = SeedsTable(seed=request.json.get("seed")).save()
    except:
        abort(400)
    return seed.to_dict(), 201


@api.route("/seed/<group_id>/comments/")
def get_seed_comments(group_id):
    seed = SeedsTable.query.get_or_404(group_id)
    return {"comments": [comment.to_dict() for comment in seed.comments]}


@api.route("/user/<string:pubkey>/seed/<group_id>/", methods=["POST"])
def get_user_seed_comment(pubkey, group_id):
    user = UsersTable.query.filter_by(pubkey=pubkey).first_or_404()
    seed = SeedsTable.query.get_or_404(group_id)
    try:
        comment = CommentsTable(
            commenttext=request.json.get("commenttext"),
            stars=request.json.get("stars"),
            group_id=seed.group_id,
            creator=user.pubkey,
        ).save()
    except:
        abort(400)
    return comment.to_dict(), 201


@api.route("/seed/<group_id>/", methods=["POST"])
def add_seed_comment(group_id):
    seed = SeedsTable.query.get_or_404(group_id)
    try:
        comment = CommentsTable(
            commenttext=request.json.get("commenttext"),
            stars=request.json.get("stars"),
            group_id=seed.group_id,
            creator="addseedbot",
        ).save()
    except:
        abort(400)
    return comment.to_dict(), 201


@api.route("/comment/<int:comment_id>/")
def get_comment(comment_id):
    comment = CommentsTable.query.get_or_404(comment_id)
    return comment.to_dict()
