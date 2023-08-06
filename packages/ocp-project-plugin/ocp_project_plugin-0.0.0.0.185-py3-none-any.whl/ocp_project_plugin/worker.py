from django_rq import job, get_queue
from django.conf import settings

import yaml
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
    print("1. Git Repo pullen")
    try:
        print("1.1 Start cloning")
        repo_instance = Repo.clone_from(GITLAB_PROJECT_URL, 'project-repo')
        print(f"1.2 Cloning finished, {repo_instance}")
    except:
        print("1.2 Cloning failed")

    print("2. Überprüfen ob es einen Branch mit dem Ticket Namen schon gibt")
    repo = Repo('project-repo')
    remote_refs = repo.remote().refs

    request = yaml_object['request']
    found = False
    for refs in remote_refs:
        if refs.name == 'origin/' + request:
            found = True
        # print(refs.name)

    if found:
        print("2.1 Branch existiert schon")
    else:
        print("2.1 Branch existiert noch nicht")
        branch_name = request
        current = repo.create_head(branch_name)
        current.checkout()

        print("2.2 Branch erstellt")

        repo.git.push('--set-upstream', 'origin', current)

        print("2.3 Branch gepushed")

    print("3. Read project values file")
    with open('project-repo/cluster/projects/values.yaml', 'r') as file:
        cur_yaml = yaml.safe_load(file)  # Note the safe_load

    index = -1
    for idx, project in enumerate(cur_yaml['projects']):
        if project['name'] == yaml_object['name']:
            print(f"3.1. Project already exists, Index Key: {idx}")
            index = idx

    print("4. Sync project values")
    if index > -1:
        cur_yaml['projects'][index] = yaml_object
    else:
        cur_yaml['projects'].append(yaml_object)

    print("5. Save project values")
    if cur_yaml:
        with open('project-repo/cluster/projects/values.yaml', 'w') as file:
            yaml.safe_dump(cur_yaml, file, sort_keys=False)

    changedFiles = [item.a_path for item in repo.index.diff(None)]
    if len(changedFiles) > 0:
        repo.git.add('*')
        repo.git.commit(m="Sync OCP Project")
        repo.git.push()

    print("6 Änderungen im Branch gepushed")

    repo = Repo('project-repo')
    repo.git.checkout('main')
    repo.git.merge(request)
    repo.git.push()

    remote = repo.remote(name='origin')
    remote.push(refspec=f":{request}")
    repo.delete_head(request)