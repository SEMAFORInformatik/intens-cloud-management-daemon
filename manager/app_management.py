from flask import current_app as app
import requests


def get_sessions():
    return [s for u in app.keycloak_admin.get_users()
            for s in app.keycloak_admin.get_sessions(u['id'])]


def get_open_apps():
    config_controller_url = app.config['CONFIG_CONTROLLER_URL']
    apps = requests.get(f'{config_controller_url}/app').json()
    return {cc_app: instances
            for cc_app in apps
            # filter to only have running apps in the list
            if (instances := requests.get(
                f'{config_controller_url}/app/{cc_app}').json())}


def clean():
    config_controller_url = app.config['CONFIG_CONTROLLER_URL']
    count = 0
    session_ids = [session['id'] for session in get_sessions()]
    apps = requests.get(f'{config_controller_url}/app').json()
    for cc_app in apps:
        instances = requests.get(
            f'{config_controller_url}/app/{cc_app}').json()
        for inst in instances:
            if inst.get('sessionID', None) in session_ids:
                continue

            app.logger.info(f"""Cleaning {cc_app} instance of session {
                inst["name"]}""")
            response = requests.delete(
                f'{config_controller_url}/app/{cc_app}/{inst["name"]}')

            if response.status_code == 200:
                count += 1

    return count
