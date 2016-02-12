from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from rooms.models import Room


class Command(BaseCommand):
    args = '<file>'
    help = ''

    def handle(self, *args, **options):
        for file in args:
            f = open(file, "r")
            for line in f:
                l = line.split()
                room = Room()
                room.number            = l[0]
                room.capacity          = int(l[1])
                room.description       = " ".join(l[2:])
                room.short_unlock_time = timezone.now()
                room.save()

            self.stdout.write('Successfully imported\n')
