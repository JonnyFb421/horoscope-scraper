from flask import Blueprint, render_template

index_blueprint = Blueprint('views', 'views')


@index_blueprint.route("/")
def index():
    return render_template('index.html')