#!/usr/bin/env python
# http://www.rabbitmq.com/tutorials/tutorial-two-python.html
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='dlx', exchange_type='direct')

result = channel.queue_declare(queue='dl')
queue_name = result.method.queue
channel.queue_bind(exchange='dlx',
                   routing_key='itask_queue', # x-dead-letter-routing-key
                   queue=queue_name)

print ' [*] Waiting for dead-letters. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] %r" % (properties,)
    print " [reason] : %s : %r" % (properties.headers['x-death'][0]['reason'], body)
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(callback,
                      queue='dl')

channel.start_consuming()
