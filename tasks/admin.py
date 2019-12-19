from django.contrib import admin

from . import models


class DoNotLog:
    def log_addition(self, *args, **kwargs):
        return

    def log_change(self, *args, **kwargs):
        return

    def log_deletion(self, *args, **kwargs):
        return


class YamlAdmin(DoNotLog, admin.ModelAdmin):
    list_display = ('path', 'task_count')

    def task_count(self, obj):
        return obj.tasks.count()
    task_count.short_description = 'タスク数'


class AnswerAdmin(DoNotLog, admin.ModelAdmin):
    list_display = ('id', 'task_script', 'mode', 'replaceable', 'clearly', 'short_message')
    list_filter = ('mode', 'replaceable', 'clearly')

    def task_script(self, obj):
        if len(obj.task.script) > 20:
            return f"{obj.task.script[:20]}..."
        return obj.task.script
    task_script.short_description = "スクリプト"

    def short_message(self, obj):
        if len(obj.message) > 20:
            return f"{obj.message[:20]}..."
        return obj.message
    short_message.short_description = '備考'


class TaskAdmin(DoNotLog, admin.ModelAdmin):
    list_display = ('module', 'script', 'role_name', 'role_user')
    list_filter = ('module',)

    def role_name(self, obj):
        return obj.role_version.role.name
    role_name.short_description = 'ロール名'
    role_name.admin_order_field = 'role__name'

    def role_user(self, obj):
        return obj.role_version.role.owner
    role_user.short_description = 'ユーザ名'
    role_user.admin_order_field = 'role__owner'


class RoleAdmin(DoNotLog, admin.ModelAdmin):
    list_display = ('name', 'owner', 'repository')


class RoleVersionAdmin(DoNotLog, admin.ModelAdmin):
    list_display = ('role_name', 'name', 'published_at', 'task_count')

    def role_name(self, obj):
        return f"{obj.role.owner}.{obj.role.name}"
    role_name.short_description = 'ロール名'

    def task_count(self, obj):
        return obj.tasks.count()
    task_count.short_description = 'タスク数'


admin.site.register(models.YamlFile, YamlAdmin)
admin.site.register(models.Answer, AnswerAdmin)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.RoleVersion, RoleVersionAdmin)
