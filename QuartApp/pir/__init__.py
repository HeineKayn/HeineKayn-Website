from quart import Blueprint, redirect

# ---------------

pirBP = Blueprint('pir', __name__, template_folder='templates', static_folder='static')

# ---------------

from .routes.home import homeBP
pirBP.register_blueprint(homeBP,url_prefix='/home')

from .routes.chart import chartBP
pirBP.register_blueprint(chartBP,url_prefix='/chart')

from .routes.candidats import candidatsBP
pirBP.register_blueprint(candidatsBP,url_prefix='/candidats')

from .routes.comparateur import comparateurBP
pirBP.register_blueprint(comparateurBP,url_prefix='/comparateur')

from .routes.aboutUs import aboutUsBP
pirBP.register_blueprint(aboutUsBP,url_prefix='/aboutUs')

from .routes.howItWorks import howItWorksBP
pirBP.register_blueprint(howItWorksBP,url_prefix='/howItWorks')


# ---------------

@pirBP.route("/")
async def hello():
    return redirect("/pir/home") # à changer