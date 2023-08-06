import logging
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler


class Logger:
    def __init__(self, log_name, credentials) -> None:
        self.log_name = log_name
        self.__credentials = credentials
        self.logger = None

    def get_logger(self):
        # Create a handler for Google Cloud Logging.
        gcloud_logging_client = google.cloud.logging.Client(
            credentials=self.__credentials
        )
        gcloud_logging_handler = CloudLoggingHandler(
            gcloud_logging_client, name=self.log_name
        )
        # Create a stream handler to log messages to the console.
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.WARNING)
        # Now create a logger and add the handlers:
        logger = logging.getLogger(self.log_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(gcloud_logging_handler)
        logger.addHandler(stream_handler)
        gcloud_logging_client.setup_logging()
        self.logger = logger
        return self.logger