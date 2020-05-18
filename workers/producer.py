#!/usr/bin/env python
import json
import os

import pika

EXCHANGE = ''
QUEUE = 'game'
ROUTING_KEY = 'game'

connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue=QUEUE)

print(os.getcwd())
content = open(os.getcwd() + '/workers/sample.json').read()
print("content", json.dumps(content))
channel.basic_publish(exchange=EXCHANGE, routing_key=ROUTING_KEY, body=json.dumps(content))
print(" [x] Data send")
connection.close()

