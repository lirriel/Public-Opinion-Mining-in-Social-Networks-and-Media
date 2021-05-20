#!/usr/bin/env python
import pika

if __name__ == '__main__':
    parameters = pika.URLParameters('RMQ_LINK')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='QUEUE_NAME', durable=True)

    messages = [] #list of accounts or tags for uploading

    for message in messages:
        channel.basic_publish(
            exchange='',
            routing_key='QUEUE_NAME',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,
            ))
        print(" [x] Sent %r" % message)
    connection.close()
