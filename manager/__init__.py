from flask import Flask, jsonify
from keycloak import KeycloakAdmin
import platform
import logging
import manager.config as config


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)


def make_app():
    app = Flask(__name__,)
    app.config.from_object(config.Config())

    app.logger.info("{'name': '%s',  'version': '%s'}",
                    config.name, app.config['VCS_INFO'])

    app.keycloak_admin = KeycloakAdmin(
        server_url=app.config['KEYCLOAK_URL'],
        username=app.config['KEYCLOAK_USERNAME'],
        password=app.config['KEYCLOAK_PASSWORD'],
        realm_name=app.config['KEYCLOAK_REALM'],
        user_realm_name='master')

    @app.route('/info', methods=['GET'])
    def get_info():
        """return info"""
        info = dict(status='UP', hostname=platform.node(),
                    rev=app.config['VCS_INFO'])
        return jsonify(info)

    from manager.routes import bp
    app.register_blueprint(bp)

    from manager.metrics import bp
    app.register_blueprint(bp)

    return app
