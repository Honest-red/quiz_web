from datetime import timedelta, time, datetime

from django.core.mail import mail_admins
from django.core.management import BaseCommand
from django.utils import timezone
from django.utils.timezone import make_aware

from quiz.models import Result

today = timezone.now()
yesterday = today - timedelta(1)
today_start = make_aware(datetime.combine(yesterday, time()))
today_end = make_aware(datetime.combine(today, time()))


class Command(BaseCommand):
    help = "Send Hello"

    def handle(self, *args, **options):
        results = Result.objects.filter(update_timestamp__range=(today_start, today_end))

        if results:
            message = ""

            for result in results:
                message += f"{result.user} \n"

            subject = (
                f"Please check test"
            )

            mail_admins(subject=subject, message=message, html_message=None)

            self.stdout.write("E-mail Report was sent.")
        else:
            self.stdout.write("No orders confirmed today.")
