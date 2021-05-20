import subprocess
import asyncio
from elasticsearch import Elasticsearch
import json
import pika
import time


async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')


def send_json(content):
    for r in content['GraphImages']:
        location = ({} if r.get('location', {}) is None else r.get('location', {})).get('address_json', None)
        if location is not None:
            location = json.loads(location)
        doc = {
            'id': r['id'],
            'owner_id': r.get('owner_id', None),
            'location': location,
            'likes': r.get('edge_liked_by', {}).get('count', None),
            'taken_at_timestamp': r['taken_at_timestamp'] * 1000,
            'tags': r.get('tags', []),
            'edge_media_to_caption': r['edge_media_to_caption'],
            'edge_media_to_comment': {
                'count': r['edge_media_to_comment']['count'],
                'data': {
                    'text': [t['text'] for t in r['edge_media_to_comment'].get('data', [])]
                }
            }
        }

        es.index(index='instagram', body=doc, id=r['id'])


if __name__ == '__main__':
    es = Elasticsearch(['ELASTIC_LINK'])

    parameters = pika.URLParameters('RMQ_LINK')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='NAME_OF_QUEUE', durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')


    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        time.sleep(body.count(b'.'))
        tag = body.decode("utf-8")
        print(f'running for {tag}')

        subprocess.run(["instagram-scraper", tag, "--latest", "--comments",
                        "--profile-metadata", "--include-location",
                        "--media-metadata", "--profile-metadata", "--media-types", "none",
                        "--retry-forever",
                        "--maximum=2000"])

        filename = tag + '/' + tag + '.json'
        with open(filename) as f:
            c = json.load(f)
            send_json(c)
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)


    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='NAME_OF_QUEUE', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()
