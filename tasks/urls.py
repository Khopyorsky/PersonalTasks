from django.urls import path, include

from tasks.views import *

app_name = 'tasks'

task_urls = [
    path('<slug:task_slug>/', TaskView.as_view(), name='page'),
    path('<slug:task_slug>/update/', UpdateTaskView.as_view(), name='update'),
    path('<slug:task_slug>/delete/', DeleteTaskView.as_view(), name='delete')
]

urlpatterns = [
    path('', TasksListView.as_view(), name='tasks'),
    path('task/', include((task_urls, 'tasks'), namespace='task')),
    path('add_task/', AddTaskView.as_view(), name='add_task'),
    path('tag/<slug:tag_slug>', TasksListView.as_view(), name='tag')
]
