from django.db import models
from django.contrib import admin


class Student(models.Model):
    """ Represents a student that is exposed via the API. """

    # ================
    # STUDENT / USERS PROPERTIES
    # ================
    # Please also look at LocalStudent model to make these overwritable.

    # CORE
    eid = models.IntegerField(unique=True)  #: Employee ID
    active = models.BooleanField()

    # User identification
    email = models.EmailField()  #: Email
    username = models.SlugField()  #: Campusnet username

    # Name
    firstName = models.TextField(blank=True)  #: First name
    lastName = models.TextField(blank=True)  #: Last name

    @property
    def fullName(self):
        """ The full name of the student. """

        return '%s %s' % (self.firstName, self.lastName)

    # Colorfoul Info
    country = models.TextField(null=True)  #: Country of origin
    picture = models.FileField(null=True)  #: Picture (if available)

    # College Contact Info
    KRUPP = 'Krupp'
    MERCATOR = 'Mercator'
    COLLEGE_III = 'C3'
    COLLEGE_NORDMETALL = 'Nordmetall'
    college = models.CharField(choices=(
        (KRUPP, 'Krupp College'),
        (MERCATOR, 'Mercator College'),
        (COLLEGE_III, 'College III'),
        (COLLEGE_NORDMETALL, 'College Nordmetall')
    ), null=True, max_length=255)

    # Physical contact information
    phone = models.TextField(blank=True, null=True)
    isCampusPhone = models.BooleanField(default=False)
    room = models.TextField(blank=True, null=True)
    building = models.CharField(null=True, max_length=255)

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
    GUEST = 'guest'
    status = models.CharField(choices=(
        (FOUNDATION_YEAR, 'Foundation Year'),
        (UNDERGRADUATE, 'Undergraduate'),

        (MASTER, 'Master'),
        (PHD_INTEGRATED, 'integrated PhD'),

        (PHD, 'PhD'),

        (WINTER, 'Winter School Student'),
        (GUEST, 'Guest Student')
    ), null=True, max_length=255)  #: current student status

    #: Degree Status
    BACHELOR_OF_SCIENCE = 'Bachelor of Science'
    BACHELOR_OF_ART = 'Bachelor of Art'
    MASTER_OF_SCIENCE = 'Master of Science'
    MASTER_OF_ART = 'Master of Art'
    PHD_DEGREE = 'PhD'
    degree = models.CharField(choices=(
        (BACHELOR_OF_SCIENCE, 'Bachelor of Science'),
        (BACHELOR_OF_ART, 'Bachelor of Art'),

        (MASTER_OF_SCIENCE, 'Master of Science'),
        (MASTER_OF_ART, 'Master of Art'),

        (PHD_DEGREE, 'PhD')
    ), null=True, max_length=255)

    # year and major
    year = models.PositiveIntegerField(
        null=True)  #: (Last known) year of Graduation
    majorShort = models.CharField(null=True, max_length=255)

    # TODO: Fill this
    MAJOR_NAMES_MAP = {
        'CS': 'Computer Science'
    }

    @property
    def major(self) -> str:
        majorShort = self.majorShort

        if majorShort in Student.MAJOR_NAMES_MAP:
            return Student.MAJOR_NAMES_MAP[majorShort]
        else:
            return None

    def localise(self, save=True):
        """ Localises this student by merging with a local object.

        :param save: If set to False, will not auto-save the given object.
        :type save: bool
        """

        # try to get the LocalStudent
        try:
            local = LocalStudent.objects.get(eid=self.eid)
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
        sdict = {
            "eid": data["eid"],
            "active": data["active"],

            "email": data["email"],
            "username": data["username"],

            "phone": data["phone"] or None,
            "isCampusPhone": data["isCampusPhone"] or False,

            "room": data["room"] or None,
            "building": data["building"] or None,

            "country": data["country"] or None,

            "firstName": data["firstName"],
            "lastName": data["lastName"],

            "isStudent": data["isStudent"],
            "isFaculty": data["isFaculty"],
            "isStaff": data["isStaff"],

            "majorShort": data["majorShort"],
        }

        # set the college according to this map
        collegeMap = {
            'Krupp': Student.KRUPP,
            'Mercator': Student.MERCATOR,
            'C3': Student.COLLEGE_III,
            'Nordmetall': Student.COLLEGE_NORDMETALL
        }

        try:
            sdict["college"] = collegeMap[data["college"]]
        except KeyError:
            sdict["college"] = None

        # try to parse the year
        try:
            sdict["year"] = int(data["year"])
        except ValueError:
            sdict["year"] = None

        # set the status according to this map
        statusMap = {
            'foundation-year': Student.FOUNDATION_YEAR,
            'undergrad': Student.UNDERGRADUATE,
            'master': Student.MASTER,
            'phd-integrated': Student.PHD_INTEGRATED,
            'phd': Student.PHD,
            'guest': Student.GUEST
        }

        try:
            sdict["status"] = statusMap[data["status"]]
        except KeyError:
            sdict["status"] = None

        # Set the degree according to this map
        degreeMap = {
            'Bachelor of Science': Student.BACHELOR_OF_SCIENCE,
            'Bachelor of Art': Student.BACHELOR_OF_ART,
            'Master of Science': Student.MASTER_OF_SCIENCE,
            'Master of Art': Student.MASTER_OF_ART,
            'PhD': Student.PHD_DEGREE
        }

        try:
            sdict["degree"] = degreeMap[data["degree"]]
        except KeyError:
            sdict["degree"] = None

        return sdict

    @classmethod
    def refresh_from_ldap(cls, username: str, password: str) -> bool:
        """ Refreshes all users from ldap and the LocalStudent db"""

        from tqdm import tqdm

        # Load all the users from LDAP
        print('** READING DATA FROM LDAP **')
        from jacobsdata.parsing import user
        users = user.parse_all_users(username, password)

        # if we get no users, there was     an error in authentication
        if users in None:
            return False

        # mark all of the current ones inactive
        print('** DISABLING OLD USERS **')
        cls.objects.all().update(active=False)

        print('** UPDATING USERS **')

        for u in tqdm(users):
            s = Student.from_json(u)
            eid = s.pop("eid")

            (stud, sup) = cls.objects.update_or_create(eid=eid, defaults=s)
            stud.localise()

        # and we are done
        return True

    def __str__(self):
        return '%s %s' % (
            self.username, '(inactive)' if not self.active else '')


class LocalStudent(models.Model):
    # ================
    # STUDENT / USERS PROPERTIES
    # ================
    # these are the local versions which can be overwritten.

    eid = models.IntegerField(unique=True)

    def merge_with(self, student):
        """ Merges this LocalStudent instance into a student instance. """

        # Iterate over all the fields
        for field in self._meta.fields:

            # read the value
            value = getattr(self, field.name)

            # and if it is not None, overwrite
            if value is not None:
                setattr(student, field.name, value)


# ENABLE SEARCHING

class AdminStudent(admin.ModelAdmin):
    search_fields = ["eid", "username"]


admin.site.register(Student, AdminStudent)
admin.site.register(LocalStudent, AdminStudent)
