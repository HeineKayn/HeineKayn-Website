from quart import Blueprint, render_template, redirect, url_for

aboutUsBP = Blueprint('aboutUs', __name__)

@aboutUsBP.route("/")
async def acceuil():
    return await render_template('aboutUs.html')

