from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'task_content', 'created_by', 'time_created', 'time_updated', 'in_progress']
    list_display_links = ['name']
    search_fields = ['name', 'detailed_descr']
    list_editable = ['in_progress']

    @admin.display
    def task_content(self, obj):
        return obj.detailed_descr[:80]
