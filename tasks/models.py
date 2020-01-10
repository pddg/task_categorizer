from django.db import models


class Mode(models.TextChoices):
    """ファイルシステムへの影響"""
    READ_ONLY = 'R', "Read only"
    WRITABLE = 'W', "Writable"
    UNKNOWN = 'U', 'Either can be read-only or write'


class NotReplaceableReason(models.TextChoices):
    """置き換え不可能な理由"""
    NOT_SUPPORTED = 'NS', 'サポートしていない操作である'
    TOO_COMPLICATE = 'TC', '複雑になりすぎる'
    CANNOT_JUDGE = 'CJ', '判断できない'
    COMPATIBILITY = 'C', '互換性のため'
    BUG = 'B', 'モジュールがバグを含むため'
    NO_CHOICE = 'NC', '---'


class Category(models.Model):
    """そのタスクの属するカテゴリ"""
    name = models.CharField(verbose_name="カテゴリ名",
                            max_length=255,
                            unique=True)

    def __str__(self):
        return self.name


class Answer(models.Model):
    """分類結果"""

    # そのタスクはファイルシステムへ影響を与えるかどうか
    mode = models.TextField(verbose_name='モード',
                            max_length=1,
                            choices=Mode.choices,
                            default=Mode.READ_ONLY)
    # そのモジュールが置き換え可能かどうか
    replaceable = models.BooleanField(verbose_name='置き換え可能',
                                      default=False)
    # 置き換えることができない理由
    reason = models.TextField(verbose_name="置き換え不可能である理由",
                              max_length=2,
                              choices=NotReplaceableReason.choices,
                              default=NotReplaceableReason.NO_CHOICE)
    # 客観的に見てわかりやすい事例であればTrue
    clearly = models.BooleanField(verbose_name='わかりやすい', default=False)
    # 代替可能モジュールの名称
    alternate_module = models.CharField(verbose_name="代替可能モジュール",
                                        max_length=30,
                                        default=None,
                                        blank=True,
                                        null=True)
    message = models.TextField(verbose_name='備考', default="", blank=True)
    task = models.OneToOneField('Task',
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True,
                                related_name='answer')
    # そのタスクが属するカテゴリ
    category = models.ForeignKey('Category',
                                 on_delete=models.SET_NULL,
                                 related_name='answers',
                                 null=True,
                                 blank=True)

    def __str__(self):
        return f"{self.task_id} - {self.message[:15]}"


class AnsibleModule(models.TextChoices):
    """モジュールの選択肢"""
    COMMAND = 'C', 'command'
    SCRIPT = 'SC', 'script'
    RAW = 'R', 'raw'
    SHELL = 'SH', 'shell'


class YamlFile(models.Model):
    """各タスクを記述しているYAMLファイル"""

    path = models.CharField(verbose_name='ファイルパス', max_length=255)
    content = models.TextField(verbose_name='コンテンツ')

    def __str__(self):
        return self.path


class RoleVersion(models.Model):
    """各ロールのバージョン"""

    name = models.CharField(verbose_name='バージョン名', max_length=255)
    min_ansible_version = models.CharField(verbose_name='最小Ansibleバージョン', max_length=10)
    published_at = models.DateTimeField(verbose_name='公開日')
    role = models.ForeignKey('Role',
                             on_delete=models.CASCADE,
                             related_name='versions')

    def __str__(self):
        return f"{self.role}-{self.name}"


class Role(models.Model):
    """ロールのメタデータ"""

    name = models.CharField(verbose_name='ロール名', max_length=255)
    owner = models.CharField(verbose_name='ユーザ', max_length=255)
    repository = models.URLField(verbose_name='リポジトリ')

    def __str__(self):
        return f"{self.owner}.{self.name}"


class Task(models.Model):
    """各バージョンがもつタスク"""

    name = models.CharField(verbose_name="name", max_length=255)
    module = models.CharField(max_length=2,
                              verbose_name='module',
                              choices=AnsibleModule.choices,
                              default=AnsibleModule.COMMAND)
    script = models.TextField(verbose_name="script")
    role_version = models.ForeignKey('RoleVersion',
                                     on_delete=models.CASCADE,
                                     related_name='tasks')
    yaml = models.ForeignKey('YamlFile',
                             on_delete=models.CASCADE,
                             related_name='tasks')
    raw = models.TextField(verbose_name='Raw task')

    def __str__(self):
        return f"{self.script}"
