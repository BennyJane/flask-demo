from .application import app, manager
from flask_script import Server

manager.add_command("run",
                    Server(host="localhost", port=app.config['SERVER_PORT'], use_debugger=app.config['DEBUG'],
                           use_reloader=True))

manager.add_command("")

if __name__ == '__main__':
    pass
