from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from presentations.models import Presentation


class Command(BaseCommand):
    help = "作成から1日経った発表を削除する 。"

    def handle(self, *args, **options):
        one_day_ago = timezone.now() - timedelta(days=1)

        old_presentations = Presentation.objects.filter(created_at__lt=one_day_ago)
        count = old_presentations.count()

        old_presentations.delete()

        self.stdout.write(self.style.SUCCESS(f"{count}件の古い発表を削除しました"))
