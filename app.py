import logging
import threading
from server import server
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    server.run()