import dataclasses
import random

from flask import flash, redirect, render_template, request, url_for
from rumpy.types.data import is_seed

from app.main import main
from app.main.forms import CommentForm, SeedForm
from app.models import CommentsTable, SeedsTable


# 主页
@main.route("/")
def index():
    return redirect(url_for("main.seeds_overview"))


# 种子一览
@main.route("/seeds/", methods=["GET", "POST"])
def seeds_overview():
    seeds = SeedsTable.query.filter_by()
    return render_template("overview.html", seeds=seeds)


def _get_user():
    return "web.share"


# 种子一览（用户发的的）
@main.route("/seeds/<pubkey>/", methods=["GET", "POST"])
def seeds_overview_user(pubkey="444"):
    seeds = SeedsTable.query.filter_by(pubkey=pubkey)
    return redirect(url_for("main.seeds_overview_user", pubkey=pubkey))


# 查询一条seed的独立页面，并提价评论
@main.route("/seed/<group_id>/", methods=["GET", "POST"])
def seed_info(group_id):
    _seed = SeedsTable.query.filter_by(group_id=group_id).first_or_404()
    form = CommentForm()
    if form.validate_on_submit():
        try:
            CommentsTable(
                commenttext=form.text.data,
                stars=form.stars.data,
                group_id=_seed.group_id,
                creator=_get_user(),
            ).save()
            flash("A new comment is successfully saved.")
            return redirect(url_for("main.seed_info", group_id=group_id))
        except:
            flash("Something went wrong, report to the admin. Thank you.")
    return render_template("comment.html", seed=_seed, form=form)


def check_seed(formdata):
    try:
        seed = json.loads(formdata)
        if is_seed(seed):
            return seed
        return None
    except:
        return None


# 添加一条seed
@main.route("/seed/add/", methods=["GET", "POST"])
def add_seed():
    # 从请求中拿到form信息
    form = SeedForm()
    if form.validate_on_submit():
        if seed := check_seed(form.seed.data):
            seed = SeedsTable(creator=_get_user(), **seed).save()
            flash("A new seed is successfully saved.")
            return redirect(url_for("main.seed_info", group_id=seed.group_id))
        else:
            flash("Ooopps. We've got this seed.")
            return redirect(url_for("main.add_seed"))
    flash("share a seed")
    return render_template("addseed.html", form=form)
