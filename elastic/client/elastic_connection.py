from elasticsearch import Elasticsearch
import json
from config_retrieval import ReadConfig


class PythonClient:
    def __init__(self):
        cfg = ReadConfig()
        self.cfg_dic = cfg.get_config()
        config = self.cfg_dic['elastic']
        self.host = config['host']
        self.user = config['user']
        self.password = config['password']
        self.index = config['index']
        self.elastic = self.connect()

    def connect(self):
        es = Elasticsearch(['http://localhost:9200'],
                           http_auth=(self.user, self.password))
        # es = Elasticsearch(hosts="http://elastic:changeme@127.0.0.1:9200/")
        # print(es.info())
        return es

    def search_articles(self, pagination, matching_terms, date_range, news_channel):
        query = {
            "from": pagination.get("from"),
            "size": pagination.get("size"),
            "query": {
                "bool": {
                    "must": {
                        "multi_match": {
                            "query": matching_terms,
                            "type": "best_fields",
                            "fields": ["title^3", "summary^2", "text", "keywords^2"],
                            "tie_breaker": 0.3
                        }
                    },
                    "filter": [
                        {
                            "range": {
                                "publish_date": {
                                    "gte": date_range.get("start_date"),
                                    "lte": date_range.get("end_date")
                                }
                            }
                        },
                        {
                            "terms": {
                                "newspaper.keyword": news_channel
                            }
                        }
                    ]

                }
            }
        }
        query = json.dumps(query)
        print(query)
        resp = self.elastic.search(index=self.index, body=query)
        return resp


if __name__ == '__main__':
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
    # print(resp)
