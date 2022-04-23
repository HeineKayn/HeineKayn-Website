from quart import Blueprint, render_template, redirect, url_for

homeBP = Blueprint('home', __name__)

@homeBP.route("/")
async def acceuil():
    return await render_template('home.html')
