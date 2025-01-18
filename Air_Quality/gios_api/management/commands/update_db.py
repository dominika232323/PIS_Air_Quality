from django.core.management.base import BaseCommand
from gios_api.db_operations import update_db

class Command(BaseCommand):
    help = "Update the database with station data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting database update...")
        update_db()
        self.stdout.write("Database update completed!")
