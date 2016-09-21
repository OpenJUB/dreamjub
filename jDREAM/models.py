from django.db import models
from django.db.models.base import ModelBase

class Student(models.Model):
    """ Represents a student that is exposed via the API. """

    # ================
    # STUDENT / USERS PROPERTIES
    # ================
    # Please also look at LocalStudent model to make these overwritable.


    # CORE
    eid = models.IntegerField(unique = True) #: Employee ID
    active = models.BooleanField()

    # User identification
    email = models.EmailField() #: Email
    username = models.SlugField() #: Campusnet username

    # Name
    firstName = models.TextField(blank = True) #: First name
    lastName = models.TextField(blank = True) #: Last name

    @property
    def fullName(self):
        """ The full name of the student. """

        return '%s %s' % (self.firstName, self.lastName)

    # Colorfoul Info
    country = models.TextField() #: Country of origin
    picture = models.FileField(null = True) #: Picture (if available)

    # College Contact Info
    KRUPP = 'Krupp'
    MERCATOR = 'Mercator'
    COLLEGE_III = 'C3'
    COLLEGE_NORDMETALL = 'Nordmetall'
    college = models.CharField(choices = (
        (KRUPP, 'Krupp College'),
        (MERCATOR, 'Mercator College'),
        (COLLEGE_III, 'College III'),
        (COLLEGE_NORDMETALL, 'College Nordmetall')
    ), null = True)

    # Physical contact information
    phone = models.TextField(blank = True, null = True)
    isCampusPhone = models.BooleanField(default = False)
    room = models.TextField(blank = True, null = True)

    # Types of people
    isStudent = models.BooleanField()
    isFaculty = models.BooleanField()
    isStaff = models.BooleanField()

    FOUNDATION_YEAR = 'foundation-year'
    UNDERGRADUATE = 'undergrad'
    MASTER = 'master'
    PHD_INTEGRATED = 'phd-integrated'
    PHD = 'phd'
    WINTER = 'winter'
    status = models.CharField(choices = (
        (FOUNDATION_YEAR, 'Foundation Year'),
        (UNDERGRADUATE, 'Undergraduate'),
        (MASTER, 'Master'),
        (PHD_INTEGRATED, 'integrated PhD'),
        (PHD, 'PhD')
    ), null = True)


    # year and major
    year = models.PositiveIntegerField(null = True) #: (Last known) year of Graduation
    majorShort = models.CharField(null = True)

    # TODO: Fill this
    MAJOR_NAMES_MAP = {
        'CS': 'Computer Science'
    }

    @property
    def major(self):
        majorShort = self.majorShort

        if majorShort in Student.MAJOR_NAMES_MAP:
            return Student.MAJOR_NAMES_MAP[majorShort]
        else:
            return None

    def localise(self, save = True):
        """ Localises this student by merging with a local object.

        :param save: If set to False, will not auto-save the given object.
        :type save: bool
        """

        # try to get the LocalStudent
        try:
            local = LocalStudent.objects.get(eid = self.eid)
        except LocalStudent.DoesNotExist:
            return False

        # do the update
        local.update(self)
        if save:
            self.save()

        # we did it -- nice
        return True

    @classmethod
    def from_json(cls, data):
        """ Creates a new Student from JSON received from LDAP. """

        # TODO: Complete this
        return Student(
            eid = data.eid
        )

class LocalStudent(models.Model):

    # ================
    # STUDENT / USERS PROPERTIES
    # ================
    # these are the local versions which can be overwritten.

    eid = models.IntegerField(unique = True)

    def merge_with(self, student):
        """ Merges this LocalStudent instance into a student instance. """

        # Iterate over all the fields
        for field in self._meta.fields:

            # read the value
            value = getattr(self, field.name)

            # and if it is not None, overwrite
            if value is not None:
                setattr(student, field.name, value)
