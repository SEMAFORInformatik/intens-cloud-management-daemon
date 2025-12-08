import flask
from prometheus_client import Gauge, CollectorRegistry, generate_latest
from manager.app_management import get_sessions, get_open_apps

bp = flask.Blueprint('metrics', __name__)

registry = CollectorRegistry()


user_sessions = Gauge('user_sessions', 'amount of open user sessions', [
                      'user'], registry=registry)

open_apps = Gauge('open_apps', 'amount of open apps', [
                  'app', 'user'], registry=registry)


@bp.before_request
def gather_metrics():
    if hasattr(flask.current_app, 'keycloak_admin'):
        user_counter = dict()
        for s in get_sessions():
            if s['username'] not in user_counter:
                user_counter[s['username']] = 0
            user_counter[s['username']] += 1

        user_sessions.clear()

        for user, count in user_counter.items():
            user_sessions.labels(user).set(count)

    open_apps.clear()

    for app, instances in get_open_apps().items():
        per_user = dict()
        for i in instances:
            if 'username' not in i:
                continue
            if i['username'] not in per_user:
                per_user[i['username']] = 0
            per_user[i['username']] += 1

        for user, count in per_user.items():
            open_apps.labels(app, user).set(count)


@bp.get('/metrics')
def deliver():
    return generate_latest(registry)
