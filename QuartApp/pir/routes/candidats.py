from quart import Blueprint, render_template, redirect, url_for

candidatsBP = Blueprint('candidats', __name__)

@candidatsBP.route("/")
async def acceuil():
    return await render_template('candidats.html')

