import logging
from decimal import Decimal
from django.core.validators import RegexValidator
from django.db.models import CharField, BooleanField, ForeignKey, CASCADE, OneToOneField, SET_NULL, PROTECT, \
    DecimalField
from django.urls import reverse
from django_rq import get_queue

from netbox import settings
from ocp_project_plugin.choices import AppEnvironmentClusterEnvChoices, AppEnvironmentDeploymentKindChoices

from netbox.models import NetBoxModel

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG.get('ocp_project_plugin', dict())
CPU_COST = PLUGIN_SETTINGS.get('cpu_cost', '')
MEMORY_COST = PLUGIN_SETTINGS.get('memory_cost', '')
STORAGE_COST = PLUGIN_SETTINGS.get('storage_cost', '')

memory_validator = RegexValidator(r"[1-9][0-9]*(Mi|Gi)$", "The input should contain only positive Number, which ends "
                                                          "with Mi (Megabyte) or Gi (Gigabyte)")


class OCPProject(NetBoxModel):
    name = CharField(
        max_length=255,
        verbose_name="OCP Project Name",
        help_text="The ocp project name e.g. web-shop",
    )
    description = CharField(
        max_length=255,
        verbose_name="Description",
        help_text="The description of the project e.g. A web shop software",
    )
    display_name = CharField(
        max_length=255,
        verbose_name="Display name",
        help_text="Display Name of the project e.g. Web Shop Shopify"
    )
    owner = ForeignKey(
        to='tenancy.Contact',
        on_delete=PROTECT,
        related_name='ocp_project_owner',
    )
    contact = ForeignKey(
        to='tenancy.Contact',
        on_delete=PROTECT,
        related_name='ocp_project_contact',
    )
    customer = ForeignKey(
        to='tenancy.Tenant',
        on_delete=PROTECT,
        related_name='ocp_project_tenant',
    )
    docu_url = CharField(
        max_length=255,
        verbose_name="URL",
        help_text="The url of the project documentation e.g. https://confluence.com/space/project",
    )
    workload = CharField(
        max_length=255,
        verbose_name="Workload",
        help_text="The workload contents e.g. Postgres DB, nginx",
    )
    request = CharField(
        max_length=255,
        verbose_name="Jira Request",
        help_text="The jira request id e.g. TICKET1234",
    )

    clone_fields = ["name", "description", "display_name", "owner", "contact", "customer", "docu_url", "workload",
                    "request"]

    class Meta:
        ordering = ["name", "description", "display_name", "owner", "contact", "customer", "docu_url", "workload",
                    "request"]

    def __str__(self):
        return f"{self.name} ({self.display_name}-{self.customer})"

    def get_absolute_url(self):
        return reverse("plugins:ocp_project_plugin:ocpproject", kwargs={"pk": self.pk})

    @property
    def docs_url(self):
        return f'https://confluence.ti8m.ch/docs/models/OCPProject/'

    def export_yaml_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'displayName': self.display_name,
            'customer': self.customer,
            'owner': self.owner,
            'contact': self.contact,
            'workloads': self.workload,
            'request': self.request,
            'url': self.docu_url
        }

    def count_app_environments(self):
        return AppEnvironment.objects.filter(OCPProject=self).count()

    def get_all_app_environments(self):
        return AppEnvironment.objects.filter(OCPProject=self)


class AppEnvironment(NetBoxModel):
    cluster_env = CharField(
        max_length=3,
        choices=AppEnvironmentClusterEnvChoices,
        default=AppEnvironmentClusterEnvChoices.CHOICE_TST,
        verbose_name="Cluster ENV",
        help_text="The Cluster Environment",
    )
    app_env = CharField(
        max_length=20,
        verbose_name="App ENV",
        help_text="The app Env String used for creating the namespace e.g. tst",
    )
    deployment_kind = CharField(
        max_length=20,
        choices=AppEnvironmentDeploymentKindChoices,
        default=AppEnvironmentDeploymentKindChoices.DEPLOYMENT_KIND_NORMAL,
        verbose_name="Deployment Kind",
        help_text="Choose the way how the deployment should work",
    )
    mtls = BooleanField(
        default=False,
        blank=False,
        verbose_name="MTLS",
        help_text="Enable if mtls should be used",
    )
    repo = CharField(
        max_length=255,
        verbose_name="Git Repository",
        help_text="Path of git Repository, don't forget the .git at the end e.g. "
                  "https://gitlab.com/example/example-deployment-manifests.git",
    )
    branch = CharField(
        max_length=20,
        verbose_name="Git Branch",
        help_text="The git Branch of the Repository e.g. main"
    )
    access_token = CharField(
        blank=True,
        max_length=100,
        verbose_name="Git Access Token",
        help_text="The access token of the tst git repo, int & prd are automatically provided"
    )
    path = CharField(
        max_length=100,
        verbose_name="Git Path",
        help_text="Path of the deployment files e.g. overlays/tst"
    )
    egress_ip = OneToOneField(
        to='ipam.IPAddress',
        on_delete=SET_NULL,
        related_name='app_env_egress_ip',
        blank=True,
        null=True,
        verbose_name='Egress IP'
    )
    monitoring = BooleanField(
        default=True,
        verbose_name="Monitoring",
        help_text="Enable if monitoring should be used",
    )
    postgres_monitoring = BooleanField(
        default=False,
        verbose_name="Postgres Monitoring",
        help_text="Enable if postgres monitoring should be used",
    )
    requests_cpu = DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        verbose_name="CPU request",
        help_text="The CPU request value e.g. 1",
    )
    requests_memory = CharField(
        max_length=5,
        blank=True,
        verbose_name="Memory request",
        help_text="The memory value e.g. 200Mi or 1Gi",
        validators=[memory_validator],
    )
    limits_cpu = DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        verbose_name="CPU Limit",
        help_text="The CPU request value e.g. 2",
    )
    limits_memory = CharField(
        max_length=5,
        blank=True,
        verbose_name="Memory Limit",
        help_text="The CPU memory value e.g. 400Mi or 2Gi",
        validators=[memory_validator],
    )
    ocp_project = ForeignKey(OCPProject, on_delete=CASCADE, related_name="app_env_ocp_project")

    clone_fields = ["access_token", "cluster_env", "app_env", "mtls", "repo", "branch", "path", "egress_ip", "deployment_kind",
                    "monitoring", "postgres_monitoring", "ocp_project", "requests_cpu", "requests_memory", "limits_cpu",
                    "limits_memory"]

    class Meta:
        ordering = ["access_token", "cluster_env", "app_env", "mtls", "repo", "branch", "path", "egress_ip", "deployment_kind",
                    "monitoring", "postgres_monitoring", "ocp_project", "requests_cpu", "requests_memory", "limits_cpu",
                    "limits_memory"]

    def __str__(self):
        return f"{self.cluster_env}-{self.app_env} ({self.repo}-{self.branch})"

    def get_absolute_url(self):
        return reverse("plugins:ocp_project_plugin:appenvironment", kwargs={"pk": self.pk})

    @property
    def docs_url(self):
        return f'https://confluence.ti8m.ch/docs/models/AppEnvironment/'

    def save(self, *args, **kwargs):
        get_queue("default").enqueue("ocp_project_plugin.worker.pull_repository")
        super(AppEnvironment, self).save(*args, **kwargs)

    def get_cluster_color(self):
        return AppEnvironmentClusterEnvChoices.colors.get(self.cluster_env)

    def get_limits_memory_gi(self):
        if self.limits_memory is '':
            return 0
        else:
            if str(self.limits_memory).endswith('Mi'):
                return int(MEMORY_COST) * float(str(self.limits_memory)[:-2]) / 1000
            else:
                return int(MEMORY_COST) * float(str(self.limits_memory)[:-2])

    def calculate_cpu_cost(self):
        return Decimal(CPU_COST) * DecimalField().to_python(self.limits_cpu)

    def calculate_memory_cost(self):
        if self.limits_memory is '':
            return '0'
        else:
            return int(MEMORY_COST) * float(str(self.limits_memory)[:-2])
