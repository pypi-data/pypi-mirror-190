from django.db.models import Sum, FloatField, IntegerField, DecimalField
from django.db.models.functions import Cast

from netbox.views.generic import ObjectView, ObjectListView, ObjectEditView, ObjectDeleteView, BulkImportView, \
    BulkEditView, BulkDeleteView

from ocp_project_plugin.filters import OCPProjectFilter
from ocp_project_plugin.forms import (
    OCPProjectImportForm,
    OCPProjectFilterForm,
    OCPProjectForm,
    OCPProjectBulkEditForm
)
from ocp_project_plugin.models import OCPProject, AppEnvironment
from ocp_project_plugin.tables import OCPProjectTable, AppEnvironmentTable
from utilities.views import register_model_view


class OCPProjectListView(ObjectListView):
    queryset = OCPProject.objects.all()
    filterset = OCPProjectFilter
    filterset_form = OCPProjectFilterForm
    table = OCPProjectTable


class OCPProjectEditView(ObjectEditView):
    """View for editing OCP Project instance."""

    queryset = OCPProject.objects.all()
    form = OCPProjectForm
    default_return_url = "plugins:ocp_project_plugin:ocpproject_list"


class OCPProjectDeleteView(ObjectDeleteView):
    queryset = OCPProject.objects.all()
    default_return_url = "plugins:ocp_project_plugin:ocpproject_list"


class OCPProjectBulkImportView(BulkImportView):
    queryset = OCPProject.objects.all()
    model_form = OCPProjectImportForm
    table = OCPProjectTable
    default_return_url = "plugins:ocp_project_plugin:ocpproject_list"


class OCPProjectBulkEditView(BulkEditView):
    queryset = OCPProject.objects.all()
    filterset = OCPProjectFilter
    table = OCPProjectTable
    form = OCPProjectBulkEditForm


class OCPProjectBulkDeleteView(BulkDeleteView):
    queryset = OCPProject.objects.all()
    table = OCPProjectTable


@register_model_view(OCPProject)
class OCPProjectView(ObjectView):
    template_name = 'ocp_project_plugin/ocp_project/ocp_project.html'
    queryset = OCPProject.objects.all()

    def get_extra_context(self, request, instance):
        app_environment_assignments = AppEnvironment.objects.restrict(request.user, 'view').filter(
            ocp_project=instance
        )
        assignments_table = AppEnvironmentTable(app_environment_assignments, user=request.user)
        assignments_table.configure(request)

        total_cpu = 0
        total_memory = 0
        total_storage = 0
        total_cpu_cost = 0
        total_memory_cost = 0
        total_storage_cost = 0
        for app_env in app_environment_assignments:
            total_cpu_cost = + app_env.calculate_cpu_cost()
            # print(app_env.calculate_memory_cost())

        return {
            'assignments_table': assignments_table,
            'assignment_count': AppEnvironment.objects.filter(ocp_project=instance).count(),
            'app_env_list': AppEnvironment.objects.filter(ocp_project=instance),
            'total_cpu': 0,
            'total_memory': 0,
            'total_storage': 0,
            'total_cpu_cost': total_cpu_cost,
            'total_memory_cost': 0,
            'total_storage_cost': 0,
        }
