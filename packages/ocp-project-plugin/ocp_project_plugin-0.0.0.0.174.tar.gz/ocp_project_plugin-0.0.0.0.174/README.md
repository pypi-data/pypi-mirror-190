# General
## Build Project
To build the project go to login in the pypi web ui and get your token. Add your token to the local pypi config.
```
poetry config pypi-token.pypi pypi-
```
After you made changes, change the version in the files pyproject.toml and netbox_storage/__init__.py

Now you can build and publish the project.
```
poetry publish --build
```

## Use Project
Link: https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins

docker-compose build --no-cache && docker-compose build --no-cache && docker-compose up -d


## Directory structure

```
+- api - The API Classes, consitsts of Serializer, URL Mapper and Views
+- filters - Filters of the models, the implementation of the method search, for searching
+- forms - The ModelForm, ModelFilterForm, ModelImportForm, ModelBulkEditForm, the forms which will be displayed
+- migrations - DB Django Migration steps
+- tables - The ModelTable, which has the configuration on how the table looks like
+- templates
  +- netbox_storage - The detail view of each model
    +- drive - The template content of drive, with base and partition model
    +- inc - The template content box in the Virtual Machine Model
    +- partition - The template content of partition, with base and physicalvolume model
    +- physicalvolume - The template content of physicalvolume with base and linuxvolume model
    +- volumegroup - The template content of volumegroup with base, logicalvolume and physicalvolume
+- views - PhysicalvolumeListView, PhysicalvolumeView, PhysicalvolumeEditView, PhysicalvolumeDeleteView, 
           PhysicalvolumeBulkImportView, PhysicalvolumeBulkEditView, PhysicalvolumeBulkDeleteView
```
## ERM

![The ERM of the Project](documents/erm.jpg?raw=true "ERM Diagram")

## Queues / Worker

### 1. Job - add_project
1. Git Repo pullen
2. Überprüfen ob es einen Branch mit dem Ticket Namen schon gibt
3. Neuer Branch erstellen mit dem Ticket Namen
4. Secrets entschlüsseln
5. OCPPRoject/AppEnvironment Model Daten in yaml konvertieren
6. YAML Daten dem values.yaml anfügen
7. Secrets der Secrets Datei anfügen
8. Secret verschlüsseln
9. Mergen



SELECT "ocp_project_plugin_appenvironment"."id", '
 '"ocp_project_plugin_appenvironment"."created", '
 '"ocp_project_plugin_appenvironment"."last_updated", '
 '"ocp_project_plugin_appenvironment"."custom_field_data", '
 '"ocp_project_plugin_appenvironment"."cluster_env", '
 '"ocp_project_plugin_appenvironment"."app_env", '
 '"ocp_project_plugin_appenvironment"."deployment_kind", '
 '"ocp_project_plugin_appenvironment"."mtls", '
 '"ocp_project_plugin_appenvironment"."repo", '
 '"ocp_project_plugin_appenvironment"."branch", '
 '"ocp_project_plugin_appenvironment"."access_token", '
 '"ocp_project_plugin_appenvironment"."path", '
 '"ocp_project_plugin_appenvironment"."egress_ip_id", '
 '"ocp_project_plugin_appenvironment"."monitoring", '
 '"ocp_project_plugin_appenvironment"."postgres_monitoring", '
 '"ocp_project_plugin_appenvironment"."requests_cpu", '
 '"ocp_project_plugin_appenvironment"."requests_memory", '
 '"ocp_project_plugin_appenvironment"."limits_cpu", '
 '"ocp_project_plugin_appenvironment"."limits_memory", '
 '"ocp_project_plugin_appenvironment"."ocp_project_id" FROM '
 '"ocp_project_plugin_appenvironment" INNER JOIN '
 '"ocp_project_plugin_ocpproject" ON '
 '("ocp_project_plugin_appenvironment"."ocp_project_id" = '
 '"ocp_project_plugin_ocpproject"."id") LEFT OUTER JOIN "ipam_ipaddress" ON '
 '("ocp_project_plugin_appenvironment"."egress_ip_id" = "ipam_ipaddress"."id") '
 'INNER JOIN "tenancy_contact" ON ("ocp_project_plugin_ocpproject"."owner_id" '
 '= "tenancy_contact"."id") INNER JOIN "tenancy_contact" T5 ON '
 '("ocp_project_plugin_ocpproject"."contact_id" = T5."id") INNER JOIN '
 '"tenancy_tenant" ON ("ocp_project_plugin_ocpproject"."customer_id" = '
 '"tenancy_tenant"."id") WHERE '
 '"ocp_project_plugin_appenvironment"."ocp_project_id" = %s ORDER BY '
 '"ocp_project_plugin_appenvironment"."access_token" ASC, '
 '"ocp_project_plugin_appenvironment"."cluster_env" ASC, '
 '"ocp_project_plugin_appenvironment"."app_env" ASC, '
 '"ocp_project_plugin_appenvironment"."mtls" ASC, '
 '"ocp_project_plugin_appenvironment"."repo" ASC, '
 '"ocp_project_plugin_appenvironment"."branch" ASC, '
 '"ocp_project_plugin_appenvironment"."path" ASC, "ipam_ipaddress"."address" '
 'ASC, "ipam_ipaddress"."id" ASC, '
 '"ocp_project_plugin_appenvironment"."deployment_kind" ASC, '
 '"ocp_project_plugin_appenvironment"."monitoring" ASC, '
 '"ocp_project_plugin_appenvironment"."postgres_monitoring" ASC, '
 '"ocp_project_plugin_ocpproject"."name" ASC, '
 '"ocp_project_plugin_ocpproject"."description" ASC, '
 '"ocp_project_plugin_ocpproject"."display_name" ASC, "tenancy_contact"."name" '
 'ASC, T5."name" ASC, "tenancy_tenant"."name" ASC, '
 '"ocp_project_plugin_ocpproject"."docu_url" ASC, '
 '"ocp_project_plugin_ocpproject"."workload" ASC, '
 '"ocp_project_plugin_ocpproject"."request" ASC, '
 '"ocp_project_plugin_appenvironment"."requests_cpu" ASC, '
 '"ocp_project_plugin_appenvironment"."requests_memory" ASC, '
 '"ocp_project_plugin_appenvironment"."limits_cpu" ASC, '
 '"ocp_project_plugin_appenvironment"."limits_memory" ASC LIMIT 4'