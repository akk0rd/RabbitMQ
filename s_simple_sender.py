#!/usr/bin/env python

#--------!!!!!!!!----|SENDER|----!!!!!!!------------------

import pika
import sys

#connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.43.64'))
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

channel.exchange_declare(exchange='myexch.dlx', exchange_type='direct')

channel.queue_declare(queue='omytestq', durable=False, arguments={"x-max-length":20,'x-dead-letter-exchange':'myexch.dlx'}) 

for i in range(1,40):    
    channel.basic_publish(exchange='', routing_key='omytestq', body='Hello World! %r'%(i), properties=pika.BasicProperties(delivery_mode = 2,))
    print " [x] Sent 'Hello World!'"


channel.queue_declare(queue='out.dlx', durable=False,arguments={'x-message-ttl' : 10})
def callback(ch, method, properties, body):
    #channel.queue_delete(queue='mytestq')
    print " [x] %r" % (body)

channel.basic_consume(callback,
                      queue='out.dlx',
                      no_ack=True)

channel.start_consuming()
