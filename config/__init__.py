import time
import logging

conf = {
    "log_path": "server_events_(" + time.strftime("%d-%m-%Y") +").log"
}

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                                logging.FileHandler(conf["log_path"], "w"),
                                logging.StreamHandler()
                            ],
                        datefmt='%H:%M:%S', level=logging.INFO)
