from django.core.validators import RegexValidator
from django.forms import (
    CharField,
    BooleanField, PasswordInput,
)

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)
from ocp_project_plugin.models import AppEnvironment, OCPProject
from utilities.forms import DynamicModelChoiceField


memory_validator = RegexValidator(r"[1-9][0-9]*(Mi|Gi)$", "The input should contain only positive Number, which ends "
                                                          "with Mi (Megabyte) or Gi (Gigabyte)")


class AppEnvironmentForm(NetBoxModelForm):
    """Form for creating a new App Environment object."""
    #requests_memory = CharField(
    #    max_length=5,
    #    label="Memory request",
    #    help_text="The memory value e.g. 200Mi or 1Gi",
    #    validators=[memory_validator],
    #)
    ocp_project = DynamicModelChoiceField(
        queryset=OCPProject.objects.all(),
        label="OCP Project",
        help_text="Choose the ocp project e.g. web shop",
    )

    fieldsets = (
        ('OCP Project', ['ocp_project']),
        ('Environment', ('cluster_env', 'app_env')),
        ('Deployment', ('repo', 'branch', 'access_token', 'path', 'deployment_kind')),
        ('Monitoring', ('monitoring', 'postgres_monitoring')),
        ('Resources', ('limits_cpu', 'limits_memory', 'requests_cpu', 'requests_memory')),
        ('Additional Config', ('mtls', 'egress_ip')),
    )

    class Meta:
        model = AppEnvironment

        fields = ["access_token", "cluster_env", "app_env", "mtls", "repo", "branch", "path", "egress_ip", "deployment_kind", "monitoring",
                  "postgres_monitoring", "ocp_project", "requests_cpu", "requests_memory", "limits_cpu",
                  "limits_memory"]

        widgets = {
            'access_token': PasswordInput(),
        }


class AppEnvironmentFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering App Environment instances."""

    model = AppEnvironment

    app_env = CharField(
        required=False,
        label="App Env",
        help_text="The app Env String used for creating the namespace e.g. tst",
    )
    mtls = BooleanField(
        required=False,
        label="MTLS",
        help_text="Enable if mtls should be used",
    )
    repo = CharField(
        required=False,
        label="Git Repository",
        help_text="Path of git Repository, don't forget the .git at the end e.g. "
                  "https://gitlab.com/example/example-deployment-manifests.git",
    )
    branch = CharField(
        required=False,
        label="Git Branch",
        help_text="The git Branch of the Repository e.g. main"
    )
    path = CharField(
        required=False,
        label="Git Path",
        help_text="Path of the deployment files e.g. overlays/tst"
    )
    egress_ip = CharField(
        required=False,
        label="Egress IP",
        help_text="The egress IP e.g. 10.10.10.10"
    )
    monitoring = BooleanField(
        required=False,
        label="Monitoring",
        help_text="Enable if monitoring should be used",
    )
    postgres_monitoring = BooleanField(
        required=False,
        label="Postgres Monitoring",
        help_text="Enable if postgres monitoring should be used",
    )


class AppEnvironmentImportForm(NetBoxModelImportForm):
    app_env = CharField(
        label="App Env",
        help_text="The app Env String used for creating the namespace e.g. tst",
    )
    mtls = BooleanField(
        required=False,
        label="MTLS",
        help_text="Enable if mtls should be used",
    )
    repo = CharField(
        label="Git Repository",
        help_text="Path of git Repository, don't forget the .git at the end e.g. "
                  "https://gitlab.com/example/example-deployment-manifests.git",
    )
    branch = CharField(
        label="Git Branch",
        help_text="The git Branch of the Repository e.g. main"
    )
    path = CharField(
        label="Git Path",
        help_text="Path of the deployment files e.g. overlays/tst"
    )
    egress_ip = CharField(
        label="Egress IP",
        help_text="The egress IP e.g. 10.10.10.10"
    )
    monitoring = BooleanField(
        required=False,
        label="Monitoring",
        help_text="Enable if monitoring should be used",
    )
    postgres_monitoring = BooleanField(
        required=False,
        label="Postgres Monitoring",
        help_text="Enable if postgres monitoring should be used",
    )

    class Meta:
        model = AppEnvironment

        fields = ["app_env", "mtls", "repo", "branch", "path", "egress_ip", "deployment_kind", "monitoring", "postgres_monitoring",
                  "ocp_project"]


class AppEnvironmentBulkEditForm(NetBoxModelBulkEditForm):
    model = AppEnvironment

    app_env = CharField(
        required=False,
        label="App Env",
        help_text="The app Env String used for creating the namespace e.g. tst",
    )
    mtls = BooleanField(
        required=False,
        label="MTLS",
        help_text="Enable if mtls should be used",
    )
    repo = CharField(
        required=False,
        label="Git Repository",
        help_text="Path of git Repository, don't forget the .git at the end e.g. "
                  "https://gitlab.com/example/example-deployment-manifests.git",
    )
    branch = CharField(
        required=False,
        label="Git Branch",
        help_text="The git Branch of the Repository e.g. main"
    )
    path = CharField(
        required=False,
        label="Git Path",
        help_text="Path of the deployment files e.g. overlays/tst"
    )
    egress_ip = CharField(
        required=False,
        label="Egress IP",
        help_text="The egress IP e.g. 10.10.10.10"
    )
    monitoring = BooleanField(
        required=False,
        label="Monitoring",
        help_text="Enable if monitoring should be used",
    )
    postgres_monitoring = BooleanField(
        required=False,
        label="Postgres Monitoring",
        help_text="Enable if postgres monitoring should be used",
    )
