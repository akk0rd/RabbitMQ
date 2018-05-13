#!/usr/bin/env python
# http://www.rabbitmq.com/tutorials/tutorial-two-python.html
import pika
import time
import random

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='itask_queue',
  arguments={
#  'x-message-ttl' : 1000,
  "x-dead-letter-exchange" : "dlx",
  "x-max-length":2,
#  "x-dead-letter-routing-key" : "dl", # if not specified, queue's routing-key is used
}
)
print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    if 1 > 0: #random.random() < 0.5:
        ch.basic_ack(delivery_tag = method.delivery_tag)
        time.sleep(5)
        print " [x] Done"
#    else:
#        ch.basic_reject(delivery_tag = method.delivery_tag, requeue=False)
#        print " [x] Rejected"

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='itask_queue')

channel.start_consuming()
