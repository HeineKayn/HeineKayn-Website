from quart import Quart, redirect, request
import os

import quart.flask_patch
from pir.routes.cache import cache

# ---------------

from dotenv import load_dotenv

load_dotenv()
app_pass = os.getenv('APP_Pass')

# ---------------

app = Quart(__name__, static_folder=None)

from quart_auth import *

auth_manager = AuthManager(app)
app.secret_key = app_pass 
app.config.from_mapping(QUART_AUTH_COOKIE_HTTP_ONLY = False)
app.config.from_mapping(QUART_AUTH_COOKIE_SECURE    = False)
app.config.from_mapping(QUART_AUTH_COOKIE_SECURE    = False)

config = {
    "DEBUG": True,                # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app.config.from_mapping(config)
cache.init_app(app)

# ---------------

from discord.ext.ipc import Client

ipc_pass = os.getenv('IPC_Pass')
global ipc_client 
ipc_client = Client(secret_key = ipc_pass)
app.config["ipc_client"] = ipc_client

# ---------------

# from botix import botixBP
# app.register_blueprint(botixBP,url_prefix='/botix')

# from bravery import ubBlueprint
# app.register_blueprint(ubBlueprint,url_prefix='/bravery')

from pir import pirBP
app.register_blueprint(pirBP,url_prefix='/pir')

from tls import tlsBP
app.register_blueprint(tlsBP,url_prefix='/tls')

from esp import getESPDic

# ---------------

@app.route("/esp", methods=['POST'])
async def esp():
    # data = await request.form
    # func = data["func"]
    # size = int(data["size"])
    # dic = getESPDic()
    dic = {}
    return dic

# Default route
@app.route("/")
def default():
    return redirect("/pir")

# ---------------

if __name__ == "__main__":
	app.run(host="localhost", port=5000, debug=True)