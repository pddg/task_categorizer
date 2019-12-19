import base64
import csv
from datetime import datetime
from hashlib import sha1
from pathlib import Path
from typing import TYPE_CHECKING

from django.core.management.base import BaseCommand
from django.db.models.functions import SHA1

from tasks import models

if TYPE_CHECKING:
    pass

date_fmt = "%Y-%m-%d %H:%M:%S.%f"


def to_date(date_str: str) -> 'datetime':
    return datetime.strptime(date_str, date_fmt)


def get_or_create_role(line: 'dict') -> 'models.Role':
    role_name = line['role_name']
    owner = line['role_owner']
    repository = line['role_repository']
    return models.Role.objects.get_or_create(name=role_name, owner=owner, repository=repository)[0]


def get_or_create_version(line: 'dict', role: 'models.Role') -> 'models.RoleVersion':
    version = line['role_version']
    min_ansible_version = line['min_ansible_version']
    published_at = to_date(line['published_at'])
    return models.RoleVersion.objects.get_or_create(name=version, role=role, published_at=published_at,
                                                    min_ansible_version=min_ansible_version)[0]


def get_or_create_yaml(line: 'dict') -> 'models.YamlFile':
    yaml_file = Path(line['yaml_path']).expanduser().resolve()
    if not yaml_file.exists():
        raise FileNotFoundError(f"{yaml_file} does not exists")
    with yaml_file.open('r') as f:
        content = f.read()
    digest = sha1(content.encode('utf-8')).hexdigest()
    yaml = models.YamlFile.objects. \
        annotate(content_hash=SHA1('content')). \
        filter(content_hash=digest). \
        filter(path=str(yaml_file)). \
        first()
    if yaml:
        return yaml
    return models.YamlFile.objects.create(
        path=str(yaml_file),
        content=content,
    )


def create_task(line: 'dict', yaml: 'models.YamlFile', version: 'models.RoleVersion') -> 'models.Task':
    script = line['script']
    module = line['module']
    name = line['name']
    raw_yaml = str(base64.b64decode(line['yaml'].encode("utf-8")), 'utf-8')
    return models.Task.objects.create(
        name=name,
        module=models.AnsibleModule[module.upper()],
        script=script,
        yaml=yaml,
        role_version=version,
        raw=raw_yaml,
    )


class Command(BaseCommand):
    help = 'Load tasks to categorize from given CSV'

    def add_arguments(self, parser):
        parser.add_argument('--csv', type=Path, required=True, help='Path to CSV file')

    def handle(self, *args, **options):
        csv_file = options.get('csv')
        csv_file = csv_file.expanduser().resolve()
        if not csv_file.exists():
            self.stderr.write("Specified csv does not exist.", self.style.ERROR)
            exit(1)

        with csv_file.open('r') as f:
            reader = csv.DictReader(f)
            for line in reader:
                role = get_or_create_role(line)
                version = get_or_create_version(line, role)
                yaml_file = get_or_create_yaml(line)
                task = create_task(line, yaml_file, version)
                self.stderr.write(f"Create {task}", self.style.SUCCESS)
        self.stderr.write("Done.", self.style.SUCCESS)
