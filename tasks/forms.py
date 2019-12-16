from django import forms

from .models import Answer


class AnswerPostForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = [
            'mode', 'replaceable', 'clearly', 'message', 'task'
        ]

    def __init__(self, post_request, **kwargs):
        super(AnswerPostForm, self).__init__(data=post_request, **kwargs)
        self.fields['task'].widget = forms.HiddenInput()
        task_id = kwargs.get('task_id')
        if task_id is None:
            task_id = post_request.pop('task_id')
            if task_id is None:
                raise AttributeError("Task IDが指定されていません")
        self.fields['task'].initial = task_id


