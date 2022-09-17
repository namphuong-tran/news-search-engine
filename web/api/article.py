from flask import Flask
from elastic.client.elastic_connection import PythonClient

app = Flask(__name__)

@app.route("/")
def search():
    pagination = {"from": 0, "size": 10}
    matching_terms = "2021 Australian grand pix"
    date_range = {"start_date" : "2022-09-05", "end_date" : "2022-09-15"}
    news_channel = ["BBC", "CNN"]
    client = PythonClient()
    resp = client.search_articles(
        pagination, matching_terms, date_range, news_channel)
    print("Got %d Hits:" % resp['hits']['total']['value'])
    for hit in resp['hits']['hits']:
        print("%(publish_date)s %(title)s: \n %(summary)s" %
              hit["_source"])
    # return "<p>Hello, World!</p>"
    # articles = resp['hits']['hits']
    articles = [article['_source'] for article in resp['hits']['hits']]
    # return [article.to_json() for article in articles]
    return {
        "result": articles,
        "from": pagination.get("from"),
        "size": pagination.get("size"),
    }