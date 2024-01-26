from django.core.management.base import BaseCommand
from django.utils import timezone
from CRM.models import Clent, Event
from django.db.models import Q

class Command(BaseCommand):
    help = 'Create birthday events for clients whose birthdays are one month ahead'

    def handle(self, *args, **options):
        today = timezone.now()
        one_month_later = today + timezone.timedelta(days=30)

        # Find clients with birthdays one month ahead
        clients_with_birthday = Clent.objects.filter(
            Q(birthday__month__lt=one_month_later.month) |
            (Q(birthday__month=one_month_later.month) & Q(birthday__year__lte=one_month_later.year) & ~Q(birthday__month=1))
        )
        # Create events for each client
        for client in clients_with_birthday:
            event_date = client.birthday.replace(year=today.year)

            # If the birthday is in the next year's January, adjust the event date
            if client.birthday.month == 1 and one_month_later.month == 12:
                event_date = client.birthday.replace(year=today.year + 1)
            event = Event.objects.create(
                user = client.user,
                event_type = "Birthday",
                event_description = f"Happy Birthday to {client.client_name}!",
                event_date = event_date,
                event_hour = '01',
                event_minute = '00',
                event_ampm = 'AM',
                is_completed = False,
            )

            self.stdout.write(self.style.SUCCESS(f"Created birthday event for {client.client_name}: {event}"))