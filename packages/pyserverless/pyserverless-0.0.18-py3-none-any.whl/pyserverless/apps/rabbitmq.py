# example_publisher.py
from typing import Dict, Union
import codefast as cf
import pika
from pyserverless.auth import auth
import json


class Connector(object):
    def __init__(self, amqp_url: str, queue_name: str) -> None:
        self.amqp_url = amqp_url
        self.queue_name = queue_name
        params = pika.URLParameters(amqp_url)
        params.socket_timeout = 30
        connection = pika.BlockingConnection(params)

        self.channel = connection.channel()
        self.channel.queue_declare(queue=queue_name)


class Publisher(Connector):
    def __init__(self, amqp_url: str, queue_name: str) -> None:
        super().__init__(amqp_url.strip(), queue_name.strip())

    def post(self, msg: Union[str, Dict]) -> None:
        # Alias of self.publish
        if isinstance(msg, dict):
            msg = json.dumps(msg)

        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=msg)

        cf.info("{} sent to {}".format(json.loads(msg), self.queue_name))
        return

    def publish(self, msg: str) -> None:
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=msg)
        cf.info("{} sent to {}".format(msg, self.queue_name))
        return


class Consumer(Connector):
    def __init__(self, amqp_url: str, queue_name: str) -> None:
        super().__init__(amqp_url, queue_name)
        self.channel.basic_qos(prefetch_count=10)
        return
    
    def callback(self, ch, method, properties, body):
        if self._callback(body):
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
    def consume(self, callback:callable = None) -> None:
        if callback is None:
            callback = self.callback
        self.channel.basic_consume(queue=self.queue_name,
                                   on_message_callback=callback,
                                   auto_ack=False)
        cf.info("Start consuming messages. To exit press CTRL+C")
        self.channel.start_consuming()
        return


class AMQPPublisher(Publisher):
    def __init__(self, queue_name: str, url: str = None) -> None:
        if url is None:
            url = auth.amqp_url
        super().__init__(url, queue_name)


class AMQPConsumer(Consumer):
    def __init__(self, queue_name: str, url: str = None) -> None:
        if url is None:
            url = auth.amqp_url
        super().__init__(url, queue_name)

    def _callback(self, body: str) -> bool:
        raise NotImplementedError("You must implement this method")

def post_message_to_queue(queue_name: str, msg: Union[str, Dict]) -> None:
    AMQPPublisher(queue_name).post(msg)

