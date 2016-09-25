import typing
import datetime

from . import component


class ActiveComponent(component.CourseParsingComponent):
    """ Checks if a course is active or not. """

    fields = ['whenCreated', 'whenChanged']

    def parse(self, course: dict, parsed_users: typing.List[dict]) \
            -> dict:
        # WARNING: This entire parsingcomponent is a hack
        # but we have nothing better for now
        # at least it is better than Stefans Campusnet login

        # get the dates when it was created and modified
        created = self.get_attribute(course, 'whenCreated', '')
        modified = self.get_attribute(course, 'whenChanged', '')

        # get the date of this entry
        td = created
        if modified != '':
            td = modified

        active = True

        # if we have a modification date
        if td != '':

            # get the current semester
            now = datetime.date.today()
            now_sem = self.getSemester(now.year, now.month)

            try:
                # and the course semester
                course_year = int(td[0:4])
                course_month = int(td[4:6])
                c_sem = self.getSemester(course_year, course_month)

                # if they are the same the course is 'active', else it is not
                active = (now_sem == c_sem)
            except Exception as e:
                pass

        return {
            'active': active
        }

    def getSemester(self, year: int, month: int) -> str:
        """ Returns a semester string given a year and a month. """

        # January => Fall Semester
        if month == 1:
            return "fall %d" % (year - 1)

        # February - July =>  Spring Semester
        elif month <= 7:
            return "spring %d" % (year)

        # August - December => Fall semester
        else:
            return "fall %d" % (year)
