#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='outsideDTM', durable=True, arguments={'x-message-ttl' : 1000, "x-max-length":2})

print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] In recieve callback"
    response = 'Changed: ' + body

    channel = connection.channel()
    print " [x] Receive %r" % (response)
    channel.queue_declare(queue='insideDTM', durable=True, arguments={'x-message-ttl' : 1000, "x-max-length":2})
    channel.basic_publish(exchange='', routing_key='insideDTM', body=response, properties=pika.BasicProperties(delivery_mode = 2,))

    ch.basic_ack(delivery_tag = method.delivery_tag)
    print " [x] out callback"

channel.basic_consume(callback,
                      queue='outsideDTM')

channel.start_consuming()
