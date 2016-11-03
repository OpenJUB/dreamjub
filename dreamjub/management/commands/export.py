from django.core.management import base
from jacobsdata.parsing import data, user

from getpass import getpass
import json


class Command(base.BaseCommand):
    help = 'Exports all data from LDAP and stores them inside JSON files. '

    def add_arguments(self, parser):
        parser.add_argument('--students', nargs='?', default=None,
                            help='Filename to store student data in. If ' +
                                 'omitted, will not store student data. ')
        parser.add_argument('--courses', nargs='?', default=None,
                            help='Filename to store course data in. If ' +
                                 'omitted, will not store student data. ')

        parser.add_argument('username', nargs='?', default=None,
                            help='Username to use for LDAP. If omitted, ' +
                                 'will ask for username interactively. ')
        parser.add_argument('password', nargs='?', default=None,
                            help='Password to use for LDAP. If omitted, ' +
                                 'will ask for password interactively. ')

    def handle(self, *args, **options):

        # check what to store.
        if options["students"] is not None:
            store_student = True
            student_fn = options["students"]
        else:
            store_student = False
            student_fn = None

        if options["courses"] is not None:
            store_course = True
            course_fn = options["courses"]
        else:
            store_course = False
            course_fn = None

        # if we have nothing to store, do nothing.
        if (not store_course) and (not store_student):
            self.stderr.write("No data to be stored, nothing to do. ")
            return

        # check username and password
        if options["username"] is None:
            self.stdout.write("Username: ")
            usr = input()
        else:
            usr = options["username"]

        if options["password"] is None:
            pwd = getpass("Password for %s:" % usr)
        else:
            pwd = options["password"]

        self.stdout.write("Retrieving data from LDAP ...")

        # if we have to store courses, get everything
        if store_course:
            (u, c) = data.parse_all(usr, pwd)
        # else get only users
        else:
            u = user.parse_all_users(usr, pwd)
            c = None

        self.stdout.write("Done. \n")

        # Store Student file
        if store_student:
            json.dump(u, open(student_fn, 'w'), sort_keys=False, indent=4)
            self.stdout.write("Wrote file %r.\n" % student_fn)

        # Store Courses file
        if store_course:
            json.dump(c, open(course_fn, 'w'), sort_keys=False, indent=4)
            self.stdout.write("Wrote file %r.\n" % course_fn)
