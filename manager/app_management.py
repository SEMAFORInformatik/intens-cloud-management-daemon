from flask import current_app as app
import requests
import time


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


def clean_keycloak():
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


def clean_timeout():
    config_controller_url = app.config['CONFIG_CONTROLLER_URL']
    count = 0
    apps = requests.get(f'{config_controller_url}/app').json()
    for cc_app in apps:
        instances = requests.get(
            f'{config_controller_url}/app/{cc_app}').json()
        for inst in instances:
            # if it has no marking for connectedness, we will let it run
            is_connected = inst.get('connected', 'true') == 'true'
            if is_connected:
                continue

            # get it in seconds
            last_connection = int(inst.get('lastConnection', 0)) / 1000
            if last_connection + app.config['SIMPLE_TIMEOUT'] > time.time():
                continue

            app.logger.info(f"""Cleaning {cc_app} instance of session {
                inst["name"]}""")
            response = requests.delete(
                f'{config_controller_url}/app/{cc_app}/{inst["name"]}')

            if response.status_code == 200:
                count += 1
    return count


def clean():
    if hasattr(app, 'keycloak_admin'):
        return clean_keycloak()

    return clean_timeout()
