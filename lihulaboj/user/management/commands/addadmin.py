from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Add a superuser directly'

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username = os.environ.get('ADMIN_USERNAME')
            password = os.environ.get('ADMIN_PASSWORD')
            email = os.environ.get('ADMIN_EMAIL')
            User.objects.create_superuser(username=username, password=password, email=email)
            print('Successfully add admin account.')
            print('username:    ', username)
            print('password:    ', password)
        else:
            print('Already have accounts, admin account will not be created.')