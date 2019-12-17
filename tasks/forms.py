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

    def set_task(self, task_id: int):
        self.fields['task'].widget = forms.HiddenInput()
        if task_id is None:
            raise AttributeError("Task IDが指定されていません")
        self.fields['task'].initial = task_id



