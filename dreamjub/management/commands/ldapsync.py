from django.core.management import base
from jacobsdata.parsing import data, course, user
from dreamjub import models

import json
from getpass import getpass


class Command(base.BaseCommand):
    help = 'Reloads all students from LDAP. '

    def add_arguments(self, parser):
        parser.add_argument('-u', '--username', nargs='?', default=None,
                            help='Username to use for LDAP. If omitted, ' +
                                 'will ask for username interactively. ')
        parser.add_argument('-p', '--password', nargs='?', default=None,
                            help='Password to use for LDAP. If omitted, ' +
                                 'will ask for password interactively. ')
        parser.add_argument('-s', '--students', nargs='?', default=None,
                            help='JSON file to read students from. See ' +
                                 '\'manage.py export\'')
        parser.add_argument('-c', '--courses', nargs='?', default=None,
                            help='JSON file to read courses from. See ' +
                                 '\'manage.py export\'')

    def get_credentials(self, options):
        if options["username"] is None:
            self.stdout.write("Username: ")
            user = input()
        else:
            user = options["username"]

        if options["password"] is None:
            pwd = getpass("Password for %s:" % user)
        else:
            pwd = options["password"]

        return user, pwd

    def handle(self, *args, **options):

        # Read the students json file if we have it
        if options["students"] is not None:
            with open(options["students"]) as data_file:
                studs = json.load(data_file)
        else:
            studs = None

        # Read the courses data file if we have it
        if options["courses"] is not None:
            with open(options["courses"]) as data_file:
                courses = json.load(data_file)
        else:
            courses = None

        needs_users = studs is None
        needs_courses = courses is None

        if needs_users or needs_courses:
            (u, p) = self.get_credentials(options)

            if needs_courses:
                # we need both
                if needs_users:
                    print("**READING STUDENTS AND COURSES FROM LDAP**")
                    (studs, courses) = data.parse_all(u, p)

                # we just need the courses
                else:
                    print("**READING COURSES FROM LDAP**")
                    courses = course.parse_all_courses(u, p, studs)

            # we just need users
            else:
                print("**READING USERS FROM LDAP**")
                studs = user.parse_all_users(u, p)

        else:
            (u, p) = None, None

        # Read data from ldap
        print("**UPDATING DATABASE**")

        # and parse
        models.Student.refresh_from_ldap(studs=studs)
        models.Course.refresh_from_ldap(courses=courses)
