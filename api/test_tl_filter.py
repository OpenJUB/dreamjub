from django.test import TestCase, client
from django.db import models
from api.filters import extended, builder

from dreamjub import models as core_models


class QTestCase(TestCase):
    """Helper for comparing Q objects.
    Adapted from http://jamescooke.info/comparing-django-q-objects.html"""

    def assertQEqual(self, left, right):
        """
        Assert `Q` objects are equal by ensuring that their
        unicode outputs are equal (crappy but good enough)
        """
        self.assertIsInstance(left, models.Q)
        self.assertIsInstance(right, models.Q)
        left_str = str(left)
        right_str = str(right)
        self.assertEqual(left_str, right_str)


class TLFilterTestCase(TestCase):
    def setUp(self):
        self.filter = extended.TLFilter()
        self.rf = client.RequestFactory()

        self.s1 = core_models.Student.objects.create(
            eid=1,
            active=True,
            email="test@jacobs.university",
            username="test",
            firstName="First",
            lastName="Last",
            isStudent=True,
            isFaculty=False,
            isStaff=False
        )
        self.s2 = core_models.Student.objects.create(
            eid=2,
            active=True,
            email="test@jacobs.university",
            username="two",
            firstName="Two",
            lastName="Last",
            isStudent=False,
            isFaculty=False,
            isStaff=True
        )
        self.s3 = core_models.Student.objects.create(
            eid=3,
            active=True,
            email="test@jacobs.university",
            username="three",
            firstName="Three",
            lastName="Last",
            isStudent=False,
            isFaculty=True,
            isStaff=False
        )

    def test_find_student(self):
        request = self.rf.get('/api/v1/users/', {
            'tl': 'isStudent==true'
        })
        all_students = core_models.Student.objects.all()
        result = self.filter.filter_queryset(request, all_students, None)
        expected = core_models.Student.objects.filter(pk=self.s1.pk)

        self.assertEquals(result[0], expected[0])

    def test_no_filter(self):
        request = self.rf.get('/api/v1/users/')
        all_students = core_models.Student.objects.all()
        result = self.filter.filter_queryset(request, all_students, None)

        self.assertEquals(result, all_students)


class BuilderTestCase(QTestCase):
    def setUp(self):
        self.builder = builder.QBuilder()

    def test_binary_equal(self):
        result = self.builder.translate({
            "operator": "==",
            "type": "BinaryExpression",
            "left": {"name": "a", "type": "Identifier"},
            "right": {"name": "b", "type": "Identifier"}
        })

        expected = models.Q(a__exact='b')

        self.assertQEqual(result, expected)

    def test_binary_not_equal(self):
        result = self.builder.translate({
            "operator": "!=",
            "type": "BinaryExpression",
            "left": {"name": "a", "type": "Identifier"},
            "right": {"name": "b", "type": "Identifier"}
        })

        expected = ~models.Q(a__exact='b')

        self.assertQEqual(result, expected)

    def test_binary_and(self):
        result = self.builder.translate({
            'type': 'BinaryExpression',
            'right': {
                'type': 'BinaryExpression',
                'right': {'type': 'Identifier', 'name': 'd'},
                'left': {'type': 'Identifier', 'name': 'c'},
                'operator': '=='
            },
            'left': {
                'type': 'BinaryExpression',
                'right': {'type': 'Identifier', 'name': 'b'},
                'left': {'type': 'Identifier', 'name': 'a'},
                'operator': '=='
            },
            'operator': '&'
        })

        expected = models.Q(a__exact='b') & models.Q(c__exact='d')
        self.assertQEqual(result, expected)

    def test_identifier(self):
        result = self.builder.translate({
            'type': 'Literal',
            'raw': 'abcdef',
            'value': 'abcdef'
        })

        self.assertEqual(result, 'abcdef')

    def test_unary_negation(self):
        result = self.builder.translate({
            "operator": "!",
            "argument": {
                'type': 'BinaryExpression',
                'right': {'type': 'Identifier', 'name': 'b'},
                'left': {'type': 'Identifier', 'name': 'a'},
                'operator': '=='
            },
            "type": "UnaryExpression"
        })

        expected = ~models.Q(a__exact='b')

        self.assertQEqual(result, expected)

    def test_unary_negation_2(self):
        result = self.builder.translate({
            "operator": "~",
            "argument": {
                'type': 'BinaryExpression',
                'right': {'type': 'Identifier', 'name': 'b'},
                'left': {'type': 'Identifier', 'name': 'a'},
                'operator': '=='
            },
            "type": "UnaryExpression"
        })

        expected = ~models.Q(a__exact='b')

        self.assertQEqual(result, expected)

    def test_empty_filter_error(self):
        with self.assertRaisesMessage(ValueError, "Filter was empty"):
            self.builder.translate(None)

    def test_filter_no_type(self):
        with self.assertRaisesMessage(ValueError, "Filter has no type"):
            self.builder.translate({
                "operator": "~",
                "argument": {
                    'type': 'BinaryExpression',
                    'right': {'type': 'Identifier', 'name': 'b'},
                    'left': {'type': 'Identifier', 'name': 'a'},
                    'operator': '=='
                }
            })

    def test_filter_invalid_type(self):
        with self.assertRaisesMessage(NotImplementedError,
                                      "Invalid filter type: EVAL"):
            self.builder.translate({
                "operator": "~",
                "argument": {
                    'type': 'EVAL',
                    'right': {'type': 'Identifier', 'name': 'b'},
                    'left': {'type': 'Identifier', 'name': 'a'},
                    'operator': '=='
                },
                "type": "EVAL"
            })

    def test_binary_missing_left(self):
        with self.assertRaisesMessage(ValueError,
                                      "Filter is incomplete: "):
            self.builder.translate({
                'type': 'BinaryExpression',
                'right': {'type': 'Identifier', 'name': 'b'},
                'operator': '=='
            })

    def test_binary_invalid_operator(self):
        with self.assertRaisesMessage(ValueError,
                                      "Unknown binary operator: "):
            self.builder.translate({
                'type': 'BinaryExpression',
                'right': {'type': 'Identifier', 'name': 'b'},
                'left': {'type': 'Identifier', 'name': 'a'},
                'operator': 'EVAL'
            })

    def test_unary_missing_argument(self):
        with self.assertRaisesMessage(ValueError,
                                      "Filter is missing: "):
            self.builder.translate({
                "operator": "!",
                "type": "UnaryExpression"
            })

    def test_unary_invalid_operator(self):
        with self.assertRaisesMessage(ValueError,
                                      "Unknown unary operator: "):
            self.builder.translate({
                "operator": "EVAL",
                "argument": {
                    'type': 'BinaryExpression',
                    'right': {'type': 'Identifier', 'name': 'b'},
                    'left': {'type': 'Identifier', 'name': 'a'},
                    'operator': '=='
                },
                "type": "UnaryExpression"
            })

    def test_invalid_literal_type(self):
        with self.assertRaisesMessage(NotImplementedError, "Invalid filter "
                                                           "type: "):
            self.builder.translate({
                'type': 'EVAL'
            })

    def test_literal_missing_value(self):
        with self.assertRaisesMessage(ValueError, "Invalid literal: "):
            self.builder.translate({
                'type': 'Identifier'
            })
