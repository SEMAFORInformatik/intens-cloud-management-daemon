import os
import pathlib

name = os.environ.get('FLASK_APP') or 'intens-cloud-management-daemon'


def vcs_info():
    g = pathlib.Path(__file__).parent / 'vcs.info'
    if g.exists():
        return g.read_text().strip()
    import subprocess
    try:
        p = subprocess.run(['git', 'describe'], capture_output=True)
        if p.returncode == 0:
            return p.stdout.decode().strip()
    except:
        pass
    return name.strip()


class Config(object):
    VCS_INFO = vcs_info()
    NAMESPACE = os.environ.get('JOB_NAMESPACE', 'default')
    CONFIG_MAP_SELECTOR = os.environ.get(
        'CONFIGMAP_SELECTOR', 'config-controller.semafor.ch/template')
    CONFIG_CONTROLLER_URL = os.getenv('CONFIG_CONTROLLER_URL')
    SIMPLE_TIMEOUT = int(os.getenv('SIMPLE_TIMEOUT'))
    KEYCLOAK_URL = os.getenv('KEYCLOAK_URL')
    KEYCLOAK_USERNAME = os.getenv('KEYCLOAK_USERNAME')
    KEYCLOAK_PASSWORD = os.getenv('KEYCLOAK_PASSWORD')
    KEYCLOAK_REALM = os.getenv('KEYCLOAK_REALM')
