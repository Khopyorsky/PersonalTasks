from django.urls import path

from tasks.views import *

app_name = 'tasks'

urlpatterns = [
    path('', TasksListView.as_view(), name='tasks'),
    path('task/<slug:task_slug>/', TaskView.as_view(), name='task_page'),
    path('add_task/', AddTaskView.as_view(), name='add_task'),
    path('update_task/<slug:task_slug>/', UpdateTaskView.as_view(), name='update_task')
]