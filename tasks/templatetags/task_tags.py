from django import template

register = template.Library()


@register.inclusion_tag('tasks/task_info.html', name='info')
def show_task_info(task):
    return {'task': task}


@register.filter(name='_join')
def show_performers(performers):
    return ', '.join([f"{p.first_name} {p.last_name}" for p in performers])
