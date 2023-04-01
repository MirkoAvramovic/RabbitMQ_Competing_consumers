import pika
import time
import random

def on_message_received(ch, method, properties, body):
    proccessing_time = random.randint(1,6)
    print(f"Received: {body}, will take {proccessing_time} to process")
    time.sleep(proccessing_time)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Finished processing the message")

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue='letterbox')

''' 
If basic_qos method is not specified, and there is more than one consumer, every consumer will wait to receive a new message
until the previous consumer has finished processing the previous message. 
'''
channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='letterbox', on_message_callback=on_message_received)

print("Starting Consuming")

channel.start_consuming()