from django.core.management.base import BaseCommand, CommandError
from jDREAM.models import Student

from getpass import getpass

class Command(BaseCommand):
    help = 'Reloads all students from LDAP. '

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='?', default=None, help='Username to use for LDAP. If omitted, will ask for username interactively. ')
        parser.add_argument('password', nargs='?', default=None, help='Passowrd to use for LDAP. If omitted, will ask for password interactively. ')

    def handle(self, *args, **options):
        if options["username"] is None:
            self.stdout.write("Username: ")
            try:
                user = input()
            except NameError:
                user = raw_input()
        else:
            user = options["username"]

        if options["password"] is None:
            pwd = getpass("Password for %s:" % user)
        else:
            pwd = options["password"]

        Student.refresh_from_ldap(user, pwd)
