from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, IntegerField
from wtforms.validators import Length, DataRequired

# 表单组件

# 评论 提交评论


class CommentForm(FlaskForm):
    text = TextAreaField(u"评价种子网络", validators=[DataRequired(), Length(2, 1000)])
    stars = IntegerField(u'评分 1-5', validators=[DataRequired()])
    submit = SubmitField(u"提交")


# seed 提交种子
class SeedForm(FlaskForm):
    seed = TextAreaField(u"提交种子", validators=[DataRequired(), Length(200, 2000)])
    submit = SubmitField(u"提交")
