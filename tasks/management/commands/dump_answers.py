import argparse
import csv
import sys
from typing import TYPE_CHECKING
from pathlib import Path

from django.core.management.base import BaseCommand

from tasks import models

if TYPE_CHECKING:
    from typing import List


def get_all_answers():
    answers = models.Answer.objects\
        .select_related()\
        .order_by('id')\
        .all()
    return answers


def to_csv_data(answers: "List[models.Answer]") -> "List[List[str]]":
    rows = []
    headers = ["mode", "category", "replaceable", "reason", "clearly", "alternate_module", "message"]
    rows.append(headers)
    for answer in answers:
        category = answer.category
        if category is None:
            category = ""
        else:
            category = category.name
        row = [
            answer.mode,
            category,
            answer.replaceable,
            answer.reason,
            answer.clearly,
            answer.alternate_module,
            answer.message
        ]
        rows.append(row)
    return rows


class Command(BaseCommand):

    def add_arguments(self, parser: "argparse.ArgumentParser"):
        out_opt = parser.add_mutually_exclusive_group()
        out_opt.add_argument("-o",
                             "--out",
                             type=str,
                             help="Path to output file")
        out_opt.add_argument("--stdout",
                             action="store_true",
                             default=False,
                             help="Output to stdout instead of file")

    def handle(self, *args, **options):
        to_stdout = options.get("stdout")
        out_file = options.get("out")
        if not to_stdout:
            if out_file is None or len(out_file) == 0:
                self.stderr.write("No output file is given.")
                exit(1)
            out_file = Path(out_file).expanduser().resolve()
            if not out_file.parent.exists():
                out_file.parent.mkdir(parents=True)
        answers = get_all_answers()
        rows = to_csv_data(answers)

        if to_stdout:
            to = sys.stdout
        else:
            to = open(out_file, 'w')
        try:
            writer = csv.writer(to, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerows(rows)
        except Exception as e:
            self.stderr.write(str(e))
            if not to_stdout:
                to.close()
