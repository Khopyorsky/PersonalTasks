from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Task
from .forms import TaskForm
from taggit.models import Tag


class TasksListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/show_tasks.html'
    context_object_name = 'tasks'

    tag = None

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            self.tag = tag
            return Task.objects.filter(tags=self.tag, performers=self.request.user)
        return self.model.objects.filter(performers=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TasksListView, self).get_context_data(object_list=object_list, **kwargs)
        if self.tag:
            context['tag'] = self.tag
        return context


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
    model = Task
    template_name = 'tasks/task.html'
    slug_url_kwarg = 'task_slug'
    context_object_name = 'task'


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    slug_url_kwarg = 'task_slug'
    context_object_name = 'task'
    template_name = 'tasks/confirm_delete.html'
    success_url = reverse_lazy('tasks:tasks')
