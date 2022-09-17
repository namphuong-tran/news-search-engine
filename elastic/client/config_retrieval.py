import configparser
import os


class ReadConfig:
    def __init__(self):
        self.base_dir = os.path.dirname(__file__)

    def get_config(self):
        file_path = os.path.abspath(os.path.join(self.base_dir, 'config.cfg'))
        cfg = configparser.RawConfigParser()
        cfg.read(file_path)

        dic = {}
        # elastic configuration
        elastic = 'LOCAL_ELASTIC'
        elastic_host = cfg.get(elastic, 'host')
        elastic_user = cfg.get(elastic, 'user')
        elastic_password = cfg.get(elastic, 'password')
        elastic_index = cfg.get(elastic, 'index')
        dic.update({'elastic': {'host': elastic_host, 'user': elastic_user,
                   'password': elastic_password, 'index': elastic_index}})
        return dic
