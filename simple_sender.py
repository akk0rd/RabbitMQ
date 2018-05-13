#!/usr/bin/env python

#--------!!!!!!!!----|SENDER|----!!!!!!!------------------

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.43.64'))
channel = connection.channel()

channel.queue_declare(queue='outsideDTM', durable=True, arguments={'x-message-ttl' : 1000, "x-max-length":2})

channel.basic_publish(exchange='', routing_key='outsideDTM', body='Hello World!', properties=pika.BasicProperties(delivery_mode = 2,))
print " [x] Sent 'Hello World!'"

channel = connection.channel()
channel.queue_declare(queue='insideDTM', durable=True, arguments={'x-message-ttl' : 1000, "x-max-length":2})

def callback(ch, method, properties, body):
    print " [x] In callback"
    print " [x] Received %r" % (body)

    ch.basic_ack(delivery_tag = method.delivery_tag)
    print "exit callback"

channel.basic_consume(callback,
                      queue='insideDTM')

channel.start_consuming()
