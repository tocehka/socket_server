from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from .socket_routes import EventWrapper
import logging
import os

class SocketServer:
    def __init__(self, domain="*", secret="1234567890", log=False):
        if not log:
            self.log = logging.getLogger('werkzeug')
            self.log.disabled = True
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = secret
        CORS(self.app, resources={r"*": {"origins": domain}})
        self.socketio = SocketIO(self.app)
        prepare_socket = EventWrapper(self.socketio)
        self.socketio = prepare_socket.get_socket()
        del prepare_socket
    
    def run(self):
        self.socketio.run(self.app, host=os.environ.get("HOST"), port=os.environ.get("PORT"))