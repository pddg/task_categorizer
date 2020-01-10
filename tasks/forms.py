from django import forms
from django.contrib import messages

from .models import Answer, NotReplaceableReason


class AnswerPostForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = [
            'mode', 'replaceable', 'clearly', 'message', 'task', 'reason', 'category', 'alternate_module'
        ]

    def __init__(self, *args, **kwargs):
        super(AnswerPostForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs["rows"] = 1
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = "custom-control-input"
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = "custom-select"
        self.fields['task'].widget = forms.HiddenInput()

    def set_task(self, task_id: int):
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

    def clean_category(self):
        category = self.cleaned_data['category']
        if category is None:
            self.fields['category'].widget.attrs['class'] = "custom-select is-invalid"
            self.add_error('category', forms.ValidationError('カテゴリが未選択です'))
        return category

    def clean_alternate_module(self):
        mod = self.cleaned_data['alternate_module']
        is_replaceable = self.cleaned_data['replaceable']
        if is_replaceable:
            if mod is None or len(mod) == 0:
                self.fields['alternate_module'].widget.attrs['class'] = "form-control is-invalid"
                self.add_error('alternate_module', forms.ValidationError('代替可能モジュールが未入力です'))
        return mod



