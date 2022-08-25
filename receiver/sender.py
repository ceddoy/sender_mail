import json
import os
from abc import ABC, abstractmethod
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import pika


class Connection(ABC):
    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def close(self, connect):
        pass


class SMTPsender(Connection):
    def __init__(self, from_addr, to_addr, password, message):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.password = password
        self.message = message

    def get_connection(self):
        return smtplib.SMTP_SSL(os.environ.get('SMTP_HOST'), int(os.environ.get('SMTP_PORT')))

    def run(self):
        msg = MIMEMultipart()
        msg['From'] = self.from_addr
        msg['To'] = self.to_addr
        msg['Subject'] = "Error message"
        msg.attach(MIMEText(self.message))

        server = self.get_connection()
        server.login(msg['From'], self.password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        self.close(server)

    def close(self, connect):
        connect.quit()


class Rabbitmq(Connection):
    def __init__(self, username, password, host='localhost', port=5672):
        self.username = username
        self.password = password
        self.host = host
        self.port = port

    def get_connection(self):
        credentials = pika.PlainCredentials(username=self.username, password=self.password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host, port=self.port, credentials=credentials))
        return connection.channel()

    def run(self):
        channel = self.get_connection()
        self.listen(channel)

    def listen(self, channel):
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='task_queue_error', on_message_callback=self.callback)
        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        loads = json.loads(body)
        sender = SMTPsender(loads.get('mail'), loads.get('mail'), os.environ.get('EMAIL_HOST_PASSWORD'), loads.get('msg'))
        sender.run()
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def close(self, connect):
        connect.close()
