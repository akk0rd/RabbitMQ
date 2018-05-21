#!/usr/bin/env python
import pika
import sys
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
        #host='192.168.43.64'))
channel = connection.channel()

channel.queue_declare(queue='outsideDTMq', durable=True, arguments={'x-message-ttl' : 30000, "x-max-length":20})

print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    #sys.exit(0)
    print " [x] In recieve callback"
    time.sleep(10)
#    response = 'Changed: ' + body

#    channel = connection.channel()
#    print " [x] Receive %r" % (response)
#    channel.queue_declare(queue='insideDTMq', durable=True, arguments={'x-message-ttl' : 30000, "x-max-length":20})
#    channel.basic_publish(exchange='', routing_key='insideDTMq', body=response, properties=pika.BasicProperties(delivery_mode = 2,))

    sys.exit(0)
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print " [x] out callback"

channel.basic_consume(callback,
                      queue='outsideDTMq')

channel.start_consuming()
