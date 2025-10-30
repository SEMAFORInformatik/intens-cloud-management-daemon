import flask
from manager.app_management import clean

bp = flask.Blueprint('routes', __name__)


@bp.get('/clean')
def clean_req():
    count = clean()
    return flask.jsonify({'count': count})
