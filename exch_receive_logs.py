#!/usr/bin/env python
import pika

#connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.43.64'))
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()

channel.exchange_declare(exchange='myexch.dlx',
                         exchange_type='direct')
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='myexch.dlx',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    channel.queue_declare(queue='out.dlx', durable=False, arguments={'x-message-ttl' : 10})
    response = "Non send: %r" %(body)
    channel.basic_publish(exchange='', routing_key='out.dlx', body=response, properties=pika.BasicProperties(delivery_mode = 2,))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
