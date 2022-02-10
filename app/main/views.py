from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.main import main
from app.main.forms import CommentForm, SeedForm
from app.models import CommentsTable, SeedsTable
import random 

#主页
@main.route("/")
def index():
    return redirect(url_for("main.seeds_overview"))


#种子一览
@main.route("/seeds/", methods=["GET", "POST"])
def seeds_overview():
    seeds = SeedsTable.query.filter_by()
    return render_template("overview.html",seeds=seeds)


def _get_user():
    return "undefined"


#种子一览（用户发的的）
@main.route("/seeds/<pubkey>/", methods=["GET", "POST"])
def seeds_overview_user(pubkey="444"):
    seeds = SeedsTable.query.filter_by(pubkey=pubkey)
    return redirect(url_for("main.seeds_overview_user", pubkey=pubkey))
    #return render_template("overview.html",seeds=seeds)


#查询一条seed的独立页面，并提价评论
@main.route("/seed/<group_id>/", methods=["GET", "POST"])
def seed_info(group_id):
    _seed = SeedsTable.query.filter_by(group_id=group_id).first_or_404()
    print("seed_info",_seed)
    form = CommentForm()
    if form.validate_on_submit():
        CommentsTable(
            commenttext=form.text.data, 
            stars=form.stars.data,
            group_id=_seed.group_id,
            creator= _get_user()).save()
        return redirect(url_for("main.seed_info", group_id=group_id))
    return render_template("comment.html", seed=_seed, form=form)


#添加一条seed
@main.route("/seed/add/", methods=["GET","POST"])
def add_seed():
    #从请求中拿到form信息
    form = SeedForm()
    if form.validate():
        seed = SeedsTable(form.seed.data, _get_user()).save()
        #todo 哪里检查 seed 是否已经重复？
        print('add_seed',seed)
        return redirect(url_for("main.seed_info", group_id=seed.group_id))
    return render_template("addseed.html", form=form)