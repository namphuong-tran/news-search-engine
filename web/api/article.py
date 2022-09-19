from crypt import methods
from flask import Flask, request, render_template
from elastic.client.elastic_connection import PythonClient
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

app = Flask(
    __name__, template_folder='../templates')
app.config['SECRET_KEY'] = "secret"

class SearchForm(FlaskForm):
    terms = StringField("Type something", validators=[DataRequired()])
    startdate = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    enddate = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    language = SelectMultipleField('Programming Language', 
                               choices=[
                                 ('cpp', 'C++'), 
                                 ('py', 'Python'), 
                                 ('text', 'Plain Text')
                               ])
    submit = SubmitField("Submit")

@app.route("/", methods=['GET', 'POST'])
def index():
    terms = None
    startdate = None
    enddate = None
    language = None
    form = SearchForm()
    if form.validate_on_submit():
        terms = form.terms.data
        startdate = form.startdate.data
        enddate = form.enddate.data
        language = form.language.data
        form.terms.data = None
        form.startdate.data = None
        form.enddate.data = None
        form.language.data = None

    return render_template("index.html", terms = terms, startdate = startdate, enddate = enddate, language = language, form = form)


@app.route("/search", methods=['GET', 'POST'])
def search():
    # pagination = {"from": 0, "size": 10}
    # matching_terms = "2021 Australian grand pix"
    # date_range = {"start_date" : "2022-09-05", "end_date" : "2022-09-15"}
    # news_channel = ["BBC", "CNN"]
    # client = PythonClient()
    # resp = client.search_articles(
    #     pagination, matching_terms, date_range, news_channel)
    # print("Got %d Hits:" % resp['hits']['total']['value'])
    # for hit in resp['hits']['hits']:
    #     print("%(publish_date)s %(title)s: \n %(summary)s" %
    #           hit["_source"])
    # # return "<p>Hello, World!</p>"
    # # articles = resp['hits']['hits']
    # articles = [article['_source'] for article in resp['hits']['hits']]
    # # return [article.to_json() for article in articles]
    # return {
    #     "result": articles,
    #     "from": pagination.get("from"),
    #     "size": pagination.get("size"),
    # }

    print(type(request.form.get("from")))
    print(request.form.get("size"))
    print(request.form.get("terms"))
    print(request.form.get("start_date"))
    print(request.form.get("end_date"))
    print(type(request.form.get("news_channel")))

    return "<p>Hello, World!</p>"

# Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500
