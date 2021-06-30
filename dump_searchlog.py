import json
import logging

import click
import requests
from click.decorators import option
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def dump_hits(dump_name, hits):
    with open(dump_name, 'a', encoding='utf-8') as f:
        for h in hits:
            f.write(json.dumps(h['_source'], ensure_ascii=False))
            f.write('\n')


@click.command()
@click.option('--elastic-host', default='185.208.180.212', type=str)
@click.option('--elastic-port', default=6900, type=int)
@click.option('--elastic-user', default='elastic', type=str)
@click.option('--elastic-pass', default='69.69$69+')
@click.option('--index-name', default='search_log', type=str)
@click.option('--request-size', default=500, type=int)
@click.option('--dump-name', default='files/search_log.jsonl', type=str)
def main(elastic_host, elastic_port, elastic_user, elastic_pass, index_name, request_size, dump_name):
    logging.info('connecting to elasti host')
    es = Elasticsearch(elastic_host, port=elastic_port, http_auth=(elastic_user, elastic_pass), request_timeout=30)
    body = {}

    logging.info('initializing search')
    data = es.search(index=index_name, scroll='2m', size=request_size, body=body)

    sid = data['_scroll_id']
    scroll_size = len(data['hits']['hits'])

    while scroll_size > 0:
        logging.info(f'dumping {scroll_size} results')
        dump_hits(dump_name, data['hits']['hits'])
        data = es.scroll(scroll_id=sid, scroll='2m')
        sid = data['_scroll_id']
        scroll_size = len(data['hits']['hits'])


if __name__ == '__main__':
    main()
