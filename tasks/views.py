from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .models import Task
from .forms import TaskForm


class TasksListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/show_tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return self.model.objects.filter(performers=self.request.user)


class AddTaskView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/add_task.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        task = form.save(commit=False)
        task.created_by = self.request.user
        response = super().form_valid(form)
        task = self.object
        task.performers.add(task.created_by)
        return response


class UpdateTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    slug_url_kwarg = 'task_slug'
    template_name = 'tasks/update_task.html'
    form_class = TaskForm


class TaskView(LoginRequiredMixin, DetailView):
    template_name = 'tasks/task.html'
    slug_url_kwarg = 'task_slug'
    context_object_name = 'task'
