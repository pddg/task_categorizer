from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, FormView
from django.urls import reverse

from .models import Task
from .forms import AnswerPostForm


class TaskListView(LoginRequiredMixin, ListView):
    """未処理のタスク一覧を返す"""

    template_name = 'tasks/task_list.html'
    queryset = Task.objects.filter(answer__isnull=True)


class CompletedTaskListView(LoginRequiredMixin, ListView):
    """処理済みのタスク一覧を返す"""
    template_name = 'tasks/task_list.html'
    queryset = Task.objects.filter(answer__isnull=False)


class AnswerView(LoginRequiredMixin, FormView):

    template_name = 'tasks/answer.html'

    def get_waited_task(self):
        """未処理のタスクを一つ返す"""
        return Task.objects.filter(answer__isnull=True).first()

    def get_success_url(self):
        latest_task = self.get_waited_task()
        return reverse('tasks:answer', kwargs={'task_id': latest_task.pk})

    def get_context_data(self, task_id: int, **kwargs):
        ctx = super(AnswerView, self).get_context_data(**kwargs)
        form = AnswerPostForm(None, task_id=task_id, **self.get_form_kwargs())
        ctx['form'] = form
        return ctx

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id', None)
        if task_id is None:
            task = self.get_waited_task()
        else:
            task = Task.objects.get(pk=int(task_id))
        ctx = self.get_context_data(task_id)
        return self.render_to_response(ctx)

    def form_valid(self, form: 'AnswerPostForm'):
        obj = form.save()
        messages.info(self.request, f"結果を保存しました．Task ID: {obj.task.pk}")
        return redirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        answer_form = AnswerPostForm(request.POST)
        if answer_form.is_valid():
            return self.form_valid(answer_form)
        return self.form_invalid(answer_form)
