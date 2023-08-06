from django_rq import job, get_queue
from django.conf import settings

from git import Repo

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG.get('ocp_project_plugin', dict())
GITLAB_PROJECT_URL = PLUGIN_SETTINGS.get('gitlab_project_url', '')
VALUES_PATH = PLUGIN_SETTINGS.get('jira_browse_url', '')

"""
1. Git Repo pullen
2. Überprüfen ob es einen Branch mit dem Ticket Namen schon gibt
3. Neuer Branch erstellen mit dem Ticket Namen
4. Secrets entschlüsseln
5. OCP PRoject/App Environment Model Daten in yaml konvertieren
6. Überprüfen ob OCP Project & App Environment schon existiern in values.yaml
7. YAML Daten dem values.yaml anfügen oder updaten
8. Secrets der Secrets Datei anfügen oder updaten
9. Secret verschlüsseln
10. Mergen
"""


@job("default")
def sync_project(yaml_object):
    print(yaml_object)
