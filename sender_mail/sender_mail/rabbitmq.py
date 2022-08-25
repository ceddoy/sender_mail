import pika
import json

from sender_mail import settings


class RabbitmqConsuming:
    def __init__(self, mail, msg):
        self.mail = mail
        self.msg = msg

    def generate_data_json(self):
        return json.dumps({'mail': self.mail, 'msg': self.msg})

    @staticmethod
    def _get_connection():
        credentials = pika.PlainCredentials(username=settings.RABBITMQ_DEFAULT_USER, password=settings.RABBITMQ_DEFAULT_PASS)
        return pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT, credentials=credentials))

    def run(self):
        connection = self._get_connection()
        channel = connection.channel()
        channel.queue_declare(queue='task_queue_error')

        message = self.generate_data_json()
        channel.basic_publish(exchange='', routing_key='task_queue_error', body=message)
        connection.close()
