from django import forms
from .models import *
from datetime import date


class TaskForm(forms.ModelForm):
    current_year = date.today().year

    time_to_finish = forms.DateTimeField(widget=forms.SelectDateWidget(
        years=(range(current_year, current_year + 5))),
        required=False)
    performers = forms.ModelMultipleChoiceField(required=False, label='Assistants', queryset=None)

    class Meta:
        model = Task
        fields = [
            'name',
            'detailed_descr',
            'in_progress',
            'time_to_finish',
            'performers',
            'tags'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user') if 'user' in kwargs else None
        update = kwargs.pop('update') if 'update' in kwargs else None
        super(TaskForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['performers'].queryset = get_user_model().objects.exclude(pk=user.pk)
        else:
            self.fields['performers'].queryset = get_user_model().objects.all()
        self.fields['performers'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"

        if update:
            self.fields['performers'].label = 'Performers'
