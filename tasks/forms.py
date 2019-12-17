from django import forms
from django.contrib import messages

from .models import Answer, NotReplaceableReason


class AnswerPostForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = [
            'mode', 'replaceable', 'clearly', 'message', 'task', 'reason'
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

    def clean_reason(self):
        reason = self.cleaned_data['reason']
        is_replaceable = self.cleaned_data['replaceable']
        if not is_replaceable and reason == NotReplaceableReason.NO_CHOICE.value:
            self.fields['reason'].widget.attrs['class'] = "custom-select is-invalid"
            self.add_error('reason', forms.ValidationError('置き換え不可能である時はその理由を選択する必要があります．'))
        if is_replaceable and reason != NotReplaceableReason.NO_CHOICE.value:
            self.fields['reason'].widget.attrs['class'] = "custom-select is-invalid"
            self.add_error('reason', forms.ValidationError('置き換え可能な時にこの理由は選択できません．'))
        return reason



