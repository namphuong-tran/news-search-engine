from crypt import methods
from flask import Flask, request, render_template, redirect, url_for, session
from crawler.newschannels import NewsChannels
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import ListWidget, CheckboxInput
from datetime import date
import web.api.db as db
from flask_paginate import Pagination, get_page_parameter

app = Flask(
    __name__, template_folder='../templates')
app.config['SECRET_KEY'] = "secret"


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class SearchForm(FlaskForm):
    terms = StringField("Type something", validators=[DataRequired()])
    startdate = DateField('Start Date', format='%Y-%m-%d', default=date.today,
                          validators=[DataRequired()])
    enddate = DateField('End Date', format='%Y-%m-%d', default=date.today,
                        validators=[DataRequired()])
    # create a list of value/description tuples
    channels = [(name, member.value)
                for name, member in NewsChannels.__members__.items()]
    selected_channels = MultiCheckboxField('News channels', choices=channels)
    submit = SubmitField("Submit")


@app.route("/", methods=['GET', 'POST'])
def index():
    session['terms'] = None
    session['startdate'] = None
    session['enddate'] = None
    session['selected_channels'] = None
    terms = None
    startdate = None
    enddate = None
    selected_channels = None
    articles = None
    pagination = None
    form = SearchForm()
    if form.validate_on_submit():
        # terms = form.terms.data
        # startdate = form.startdate.data
        # enddate = form.enddate.data
        # selected_channels = form.selected_channels.data
        # print(type(selected_channels))
        # print(selected_channels)
        # # resp = db.search()
        # # total = resp.get('total')
        # # articles = resp.get('result')

        # search = False
        # q = request.args.get('q')
        # if q:
        #     search = True

        # # search = True
        # total = 100
        # articles = [1,2,3,4,5,6,7,8,9,10]

        # page = request.args.get(get_page_parameter(), type=int, default=1)
        # pagination = Pagination(page=page, total=total, search=search, record_name='articles', css_framework='bootstrap5', show_single_page=True, per_page=3)
        # return render_template("index.html", terms=terms, startdate=startdate, enddate=enddate, selected_channels=selected_channels, form=form, articles=articles,
        #                    pagination=pagination)
        session['terms'] = form.terms.data
        session['startdate'] = form.startdate.data.strftime('%Y-%m-%d')
        session['enddate'] = form.enddate.data.strftime('%Y-%m-%d')
        session['selected_channels'] = form.selected_channels.data
        return redirect(url_for('search'))

    print(request.args.get(get_page_parameter(), type=int, default=1))
    return render_template("index.html", terms=terms, startdate=startdate, enddate=enddate, selected_channels=selected_channels, form=form, articles=articles,
                           pagination=pagination)


@app.route("/search", methods=['GET', 'POST'])
def search():
    terms = session['terms']
    # startdate = session['startdate']
    # enddate = session['enddate']
    date_range = {
        "start_date": session['startdate'], "end_date": session['enddate']}
    selected_channels = session['selected_channels']
    size = 10
    page = request.args.get(get_page_parameter(), type=int, default=1)
    print(page)

    pagination = {"from": (page - 1) * size, "size": size}
    resp = db.search(pagination, terms, date_range, selected_channels)
    total = resp.get("total")
    articles = resp.get("result") 

    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, total=total, record_name='articles',
                            css_framework='bootstrap5', show_single_page=True, per_page=size)
    return render_template("search.html", articles=articles, pagination=pagination)

# Custom Error Pages

# Invalid URL


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500
