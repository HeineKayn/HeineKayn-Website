from quart import Blueprint, render_template, redirect, url_for

howItWorksBP = Blueprint('howItWorks', __name__)

@howItWorksBP.route("/")
async def acceuil():
    return await render_template('howItWorks.html')

