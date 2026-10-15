from django.core.management.base import BaseCommand

from apps.surveys.seed_data import SCENARIOS
from apps.surveys.services.seed import load_scenario


class Command(BaseCommand):
    help = "Загружает сценарии опросов из apps/surveys/seed_data (по умолчанию не перезаписывает существующее)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--overwrite", action="store_true",
            help="Перезаписать существующие записи данными из файла (правки из админки будут потеряны)",
        )

    def handle(self, *args, **options):
        for data in SCENARIOS:
            stats = load_scenario(data, overwrite=options["overwrite"])
            self.stdout.write(
                f"{data['slug']}: создано записей {stats['created']}, уже было {stats['existing']}"
            )
