# Generated by Django 3.0 on 2019-12-16 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='ロール名')),
                ('owner', models.CharField(max_length=255, verbose_name='ユーザ')),
                ('repository', models.URLField(verbose_name='リポジトリ')),
            ],
        ),
        migrations.CreateModel(
            name='RoleVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='バージョン名')),
                ('published_at', models.DateTimeField(verbose_name='公開日')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='tasks.Role')),
            ],
        ),
        migrations.CreateModel(
            name='YamlFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, verbose_name='ファイルパス')),
                ('content', models.TextField(verbose_name='コンテンツ')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('module', models.CharField(choices=[('C', 'command'), ('SC', 'script'), ('R', 'raw'), ('SH', 'shell')], default='C', max_length=2, verbose_name='module')),
                ('script', models.TextField(verbose_name='script')),
                ('role_version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='tasks.RoleVersion')),
                ('yaml', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='tasks.YamlFile')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.TextField(choices=[('R', 'Read only'), ('W', 'Writable'), ('U', 'Either can be read-only or write')], default='R', max_length=1, verbose_name='モード')),
                ('replaceable', models.BooleanField(default=False, verbose_name='置き換え可能')),
                ('clearly', models.BooleanField(default=False, verbose_name='わかりやすい')),
                ('message', models.TextField(verbose_name='備考')),
                ('task', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='tasks.Task')),
            ],
        ),
    ]