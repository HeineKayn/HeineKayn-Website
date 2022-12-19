from quart import Blueprint, render_template

# ---------------

tlsBP = Blueprint('tls', __name__, template_folder='templates', static_folder='static')

# ---------------

@tlsBP.route("/")
async def hello():
    return await render_template('tls.html')