from dotenv import load_dotenv
import os
from socket_backend import createServer

if __name__ == "__main__":
    load_dotenv()
    env_secret = os.environ.get("SECRET_KEY")
    env_domain = os.environ.get("DOMAIN")
    app = createServer(env_domain, env_secret)
    app.run()