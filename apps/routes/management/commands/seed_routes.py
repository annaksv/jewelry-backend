from django.core.management.base import BaseCommand, CommandError

from apps.routes.seed_data import ROUTE_CONTENT
from apps.routes.services.seed import load_route_content
from apps.surveys.models import Scenario


class Command(BaseCommand):
    help = "Загружает блоки маршрута и правила (по умолчанию не перезаписывает существующее)"

    def add_arguments(self, parser):
        parser.add_argument("--overwrite", action="store_true",
                            help="Перезаписать существующие блоки (правки из админки будут потеряны)")

    def handle(self, *args, **options):
        for slug, blocks in ROUTE_CONTENT:
            try:
                stats = load_route_content(slug, blocks, overwrite=options["overwrite"])
            except Scenario.DoesNotExist:
                raise CommandError(f"Сценарий {slug} не найден. Сначала выполните: python manage.py seed_surveys")
            self.stdout.write(f"{slug}: блоков создано {stats['created']}, уже было {stats['existing']}")
