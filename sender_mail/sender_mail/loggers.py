from logging import StreamHandler, LogRecord, Handler

from sender_mail.rabbitmq import RabbitmqConsuming
from sender_mail.settings import EMAIL_HOST_USER


class CatchSenderErrorHandler(Handler):
    def emit(self, record: LogRecord) -> None:
        try:
            msg = self.format(record)
            queue_send = RabbitmqConsuming(EMAIL_HOST_USER, msg)
            queue_send.run()
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)
