from django.core.management import base
from dreamjub import models

from getpass import getpass


class Command(base.BaseCommand):
    help = 'Reloads all students from LDAP. '

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='?', default=None,
                            help='Username to use for LDAP. If omitted, ' +
                                 'will ask for username interactively. ')
        parser.add_argument('password', nargs='?', default=None,
                            help='Password to use for LDAP. If omitted, ' +
                                 'will ask for password interactively. ')

    def handle(self, *args, **options):
        if options["username"] is None:
            self.stdout.write("Username: ")
            user = input()
        else:
            user = options["username"]

        if options["password"] is None:
            pwd = getpass("Password for %s:" % user)
        else:
            pwd = options["password"]

        models.Student.refresh_from_ldap(user, pwd)
