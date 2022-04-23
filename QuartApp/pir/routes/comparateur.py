from quart import Blueprint, render_template, redirect, url_for

comparateurBP = Blueprint('comparateur', __name__)

@comparateurBP.route("/")
async def acceuil():
    return await render_template('comparateur.html')

