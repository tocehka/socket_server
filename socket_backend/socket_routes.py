from flask import request
import os
from flask_socketio import emit
from processing.mesure_filters import primal_filter
import logging
import config

class PairStatus:
    def __init__(self):
        self.zephyr = False
        self.unreal = False
        self.__logger = logging.getLogger("socket_routes")
    def __str__(self):
        return "PairStatus: Zephyr connection = " + str(self.zephyr) + ", Unreal connection = " + str(self.unreal)
    def ready(self):
        if self.zephyr and self.unreal:
            return True
        else:
            return False

class EventWrapper:
    def __init__(self, socketio):
        self.logger = logging.getLogger("socket_routes")
        self.logger.info("Server was started")
        self.zephyr_name = os.environ.get("ZEPHYR")
        self.unreal_name = os.environ.get("UNREAL")
        self.key = os.environ.get("CONNECTION_KEY")
        self.socketio = self.__event_wrap(socketio)
        self.pair_status = PairStatus()

    def __event_wrap(self, socketio):
        @socketio.on("connect")
        def connect():
            client_key = request.args.get("key")
            client_name = request.args.get("name")
            if client_key != self.key:
                self.logger.info(f"Client {client_name} was disconnected from server as he had an incorrect key")
                return False
            if client_name == self.zephyr_name:
                self.pair_status.zephyr = True
                emit("pair status", True, namespace="/unreal")
            elif client_name == self.unreal_name:
                self.pair_status.unreal = True
                emit("pair status", True, namespace="/zephyr")
            name = client_name.split("_")[0]
            self.logger.info(f"Client {name} sucessfully connected")
            self.logger.info(str(self.pair_status))

        @socketio.on("data reciever", namespace="/zephyr")
        def get_measure(data):
            client_name = request.args.get("name")
            name = client_name.split("_")[0]
            self.logger.info(f"From {name} was recived data: {data}")
            if self.pair_status.ready():
                stress = primal_filter(data)
                emit("stress stream", stress, broadcast=True, namespace="/unreal")
                self.logger.info("Stress indicator was sent to Unreal Engine")

        @socketio.on("disconnect")
        def disconnect():
            client_name = request.args.get("name")
            name = client_name.split("_")[0]
            self.logger.info(f"Mr {name} disconnected from server")
            if client_name == self.zephyr_name:
                self.pair_status.zephyr = False
                emit("pair status", False, namespace="/unreal")
            elif client_name == self.unreal_name:
                self.pair_status.unreal = False
                emit("pair status", False, namespace="/zephyr")

        return socketio

    def get_socket(self):
        return self.socketio