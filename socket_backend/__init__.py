from .server import SocketServer

def createServer(domain, secret):
    return SocketServer(domain, secret)