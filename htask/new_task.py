#!/usr/bin/env python
# http://www.rabbitmq.com/tutorials/tutorial-two-python.html
import pika
import sys
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

message = ' '.join(sys.argv[1:]) or "Hello World!"
for i in range (1,15):
    channel.basic_publish(exchange='',
        routing_key='itask_queue',
                      body=message+str(i),
    )
    print " [x] Sent %r" % (message+str(i),)
    time.sleep(1)
connection.close()
