from flask import blueprints, render_template

main_bp = blueprints.Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')

