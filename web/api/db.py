from elastic.client.elastic_connection import PythonClient


def search(pagination, matching_terms, date_range, selected_channels):
    client = PythonClient()
    resp = client.search_articles(
        pagination, matching_terms, date_range, selected_channels)
    print("Got %d Hits:" % resp['hits']['total']['value'])
    for hit in resp['hits']['hits']:
        print("%(publish_date)s %(title)s: \n %(summary)s" %
              hit["_source"])
    total_results = resp['hits']['total']['value']
    articles = [article['_source'] for article in resp['hits']['hits']]
    return {
        "result": articles,
        "total": total_results
    }
