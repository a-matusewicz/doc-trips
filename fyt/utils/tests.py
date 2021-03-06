import unittest

from django.core.exceptions import ValidationError
from django.template import Context, Template
from model_mommy import mommy

from fyt.test import FytTestCase
from fyt.trips.models import Section
from fyt.utils.fmt import join_with_and, join_with_or, section_range
from fyt.utils.lat_lng import parse_lat_lng, validate_lat_lng
from fyt.utils.matrix import OrderedMatrix


class OrderedMatrixTestCase(unittest.TestCase):
    def test_truncate_matrix(self):
        rows = [0, 1]
        cols = [0, 1]
        m = OrderedMatrix(rows, cols)
        m[1][1] = True
        self.assertEqual(m.truncate(), {1: {0: None, 1: True}})

    def test_map(self):
        rows = [0, 1]
        cols = [0, 1]
        m = OrderedMatrix(rows, cols, default=0)
        n = m.map(lambda x: x + 1)
        self.assertTrue(n[0][0] == n[0][1] == n[1][0] == n[1][1] == 1)

    def test_map_creates_new_instance(self):
        rows = [0, 1]
        cols = [0, 1]
        m = OrderedMatrix(rows, cols, default=0)
        n = m.map(lambda x: x + 1)
        self.assertEqual(m[0][0], 0)


class FmtUtilsTest(FytTestCase):
    def test_section_range(self):
        mommy.make(Section, name="A")
        mommy.make(Section, name="B")
        mommy.make(Section, name="C")
        self.assertEqual(section_range(Section.objects.all()), "A - C")

    def test_section_range_not_contiguous(self):
        mommy.make(Section, name="A")
        mommy.make(Section, name="C")
        with self.assertRaises(AssertionError):
            section_range(Section.objects.all())

    def test_join_with_and(self):
        self.assertEqual(join_with_and(['A']), 'A')
        self.assertEqual(join_with_and(['A', 'B']), 'A and B')
        self.assertEqual(join_with_and(['A', 'B', 'C', 'D']), 'A, B, C and D')

    def test_join_with_or(self):
        self.assertEqual(join_with_or(['A', 'B', 'C', 'D']), 'A, B, C or D')


class LatLngRegex(unittest.TestCase):
    def test_lat_lng(self):
        tests = [
            ('13.0,153.5', '13.0,153.5'),
            ('23.0, 153.5', '23.0,153.5'),
            ('33.0,153.5', '33.0,153.5'),
            ('-43.0, -153.5', '-43.0,-153.5'),
            ("""44° 2'39.67"N 71°47'31.72"W""", None),  # no match
            ('63.0,       153.5', '63.0,153.5'),
            ('73.0 153.5', '73.0,153.5'),
            # ...
        ]
        for string, target in tests:
            self.assertEqual(target, parse_lat_lng(string))

    def test_validate_lat_lng(self):
        validate_lat_lng('13.0,153.5')
        validate_lat_lng(' 13.0,153.5 ')
        with self.assertRaises(ValidationError):
            validate_lat_lng('g 13.0,153.5 ')
        with self.assertRaises(ValidationError):
            validate_lat_lng('13.0,153.5  13.0,153.5 ')


class UrlencodeTagTestCase(FytTestCase):
    def test_tag(self):
        out = Template(
            """
            {% load urlencode %}
            {% urlencode param1=value1 param2="test this" %}
            """
        ).render(Context({'value1': 1}))
        self.assertIn(
            out.strip(),
            ['param1=1&amp;param2=test+this', 'param2=test+this&amp;param1=1'],
        )
