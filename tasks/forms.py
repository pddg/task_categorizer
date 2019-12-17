from django import forms

from .models import Answer


class AnswerPostForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = [
            'mode', 'replaceable', 'clearly', 'message', 'task'
        ]

    def __init__(self, *args, **kwargs):
        super(AnswerPostForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs["rows"] = 3
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = "custom-control-input"
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = "custom-select"

    def set_task(self, task_id: int):
        self.fields['task'].widget = forms.HiddenInput()
        if task_id is None:
            raise AttributeError("Task IDが指定されていません")
        self.fields['task'].initial = task_id



