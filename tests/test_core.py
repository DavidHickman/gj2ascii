"""
Unittests for gj2ascii._core
"""


from collections import OrderedDict
import itertools
import os
import unittest

import fiona

import gj2ascii
from . import compare_ascii
import numpy as np
from . import POLY_FILE
from . import EXPECTED_POLYGON_20_WIDE


def test_compare_ascii():
    # compare_ascii() is a function that is defined within the unittests and only used for testing
    block = """
    line1
    line2
    something
    a n o t h e r line
    None
    6789.2349
    """
    assert compare_ascii(block, block) is True


class TestDictTable(unittest.TestCase):

    def test_empty_dict(self):
        with self.assertRaises(ValueError):
            gj2ascii.dict2table({})

    def test_with_values(self):
        test_dict = OrderedDict((
            ('Field1', None),
            ('__something', 'a string'),
            ('more', 12345),
            ('other', 1.2344566)
        ))
        expected = """
+-------------+-----------+
| Field1      |      None |
| __something |  a string |
| more        |     12345 |
| other       | 1.2344566 |
+-------------+-----------+
""".strip()
        self.assertEqual(gj2ascii.dict2table(test_dict), expected)


class TestRender(unittest.TestCase):

    def test_exception(self):
        with self.assertRaises(ValueError):
            gj2ascii.render([], None, fill='asdf')
        with self.assertRaises(ValueError):
            gj2ascii.render([], None, value='asdf')
        with self.assertRaises(ValueError):
            gj2ascii.render([], width=-1)

    def test_compare_bbox_given_vs_detect_collection_vs_compute_vs_as_generator(self):
        # Easiest to compare these 3 things together since they are related
        with fiona.open(POLY_FILE) as src:
            given = gj2ascii.render(src, 15, bbox=src.bounds)
            computed = gj2ascii.render([i for i in src], 15)
            fio_collection = gj2ascii.render(src, 15)
            # Passing in a generator and not specifying x/y min/max requires the features to be iterated over twice
            # which is a problem because generators cannot be reset.  A backup of the generator should be created
            # automatically and iterated over the second time.
            generator_output = gj2ascii.render((f for f in src), 15)
        for pair in itertools.combinations([given, computed, fio_collection, generator_output], 2):
            self.assertEqual(*pair)

    def test_with_fiona(self):
        with fiona.open(POLY_FILE) as src:
            r = gj2ascii.render(src, width=20, fill='.', value='+', bbox=src.bounds)
            self.assertEqual(EXPECTED_POLYGON_20_WIDE.strip(), r.strip())


class TestGeometryExtractor(unittest.TestCase):

    def setUp(self):

        class GIFeature(object):
            __geo_interface__ = {
                'type': 'Feature',
                'properties': {},
                'geometry': {
                    'type': 'Point',
                    'coordinates': [10, 20, 30]
                }
            }
        self.gi_feature = GIFeature()

        class GIGeometry(object):
            __geo_interface__ = {
                'type': 'Polygon',
                'coordinates': [[(1.23, -56.5678), (4.897, 20.937), (9.9999999, -23.45)]]
            }
        self.gi_geometry = GIGeometry()

        self.feature = {
            'type': 'Feature',
            'properties': {},
            'geometry': {
                'type': 'Line',
                'coordinates': ((1.23, -67.345), (87.12354, -23.4555), (123.876, -78.9444))
            }
        }

        self.geometry = {
            'type': 'Point',
            'coordinates': (0, 0, 10)
        }

    def test_exceptions(self):
        with self.assertRaises(TypeError):
            next(gj2ascii._core._geometry_extractor([{'type': None}]))

    def test_single_object(self):
        self.assertDictEqual(self.geometry, next(gj2ascii._core._geometry_extractor(self.geometry)))
        self.assertDictEqual(self.feature['geometry'], next(gj2ascii._core._geometry_extractor(self.feature)))
        self.assertDictEqual(
            self.gi_feature.__geo_interface__['geometry'], next(gj2ascii._core._geometry_extractor(self.gi_feature)))
        self.assertDictEqual(
            self.gi_geometry.__geo_interface__, next(gj2ascii._core._geometry_extractor(self.gi_geometry)))

    def test_multiple_homogeneous(self):
        for item in gj2ascii._core._geometry_extractor((self.geometry, self.geometry, self.geometry)):
            self.assertDictEqual(item, self.geometry)
        for item in gj2ascii._core._geometry_extractor((self.feature, self.feature, self.feature)):
            self.assertDictEqual(item, self.feature['geometry'])
        for item in gj2ascii._core._geometry_extractor((self.gi_geometry, self.gi_geometry, self.gi_geometry)):
            self.assertDictEqual(item, self.gi_geometry.__geo_interface__)
        for item in gj2ascii._core._geometry_extractor((self.gi_feature, self.gi_feature, self.gi_feature)):
            self.assertDictEqual(item, self.gi_feature.__geo_interface__['geometry'])

    def test_multiple_heterogeneous(self):
        input_objects = (self.geometry, self.feature, self.gi_feature, self.gi_geometry)
        expected = (self.geometry, self.feature['geometry'], self.gi_feature.__geo_interface__['geometry'],
                    self.gi_geometry.__geo_interface__)
        for expected, actual in zip(expected, gj2ascii._core._geometry_extractor(input_objects)):
            self.assertDictEqual(expected, actual)


class TestStack(unittest.TestCase):

    def test_standard(self):

        l1 = gj2ascii.array2ascii([['*', '*', '*', '*', '*'],
                                   [' ', ' ', '*', ' ', ' '],
                                   ['*', '*', ' ', ' ', ' ']])

        l2 = gj2ascii.array2ascii([[' ', ' ', ' ', '+', '+'],
                                   [' ', '+', ' ', ' ', ' '],
                                   [' ', ' ', '+', '+', '+']])

        eo = gj2ascii.array2ascii([['*', '*', '*', '+', '+'],
                                   ['.', '+', '*', '.', '.'],
                                   ['*', '*', '+', '+', '+']])

        self.assertEqual(gj2ascii.stack([l1, l2], fill='.').strip(os.linesep), eo.strip(os.linesep))

    def test_exceptions(self):
        # Bad fill value
        with self.assertRaises(ValueError):
            gj2ascii.stack([], fill='too-long')

        # Input layers have different dimensions
        with self.assertRaises(ValueError):
            gj2ascii.stack(['1', '1234'])

    def test_single_layer(self):
        l1 = gj2ascii.array2ascii([['*', '*', '*', '*', '*'],
                                   [' ', ' ', '*', ' ', ' '],
                                   ['*', '*', ' ', ' ', ' ']])

        self.assertTrue(compare_ascii(l1, gj2ascii.stack([l1])))


class TestArray2Ascii2Array(unittest.TestCase):

    def setUp(self):
        self.ascii = '* * * * *' + os.linesep + '  *   *  ' + os.linesep + '* * * * *'
        self.array = [['*', '*', '*', '*', '*'], [' ', '*', ' ', '*', ' '], ['*', '*', '*', '*', '*']]
        self.np_array = np.array(self.array)

    def test_ascii2array(self):
        self.assertEqual(self.array, gj2ascii.ascii2array(self.ascii))
        self.assertTrue(np.array_equal(self.np_array, np.array(gj2ascii.ascii2array(self.ascii))))

    def test_array2ascii(self):
        self.assertEqual(self.ascii, gj2ascii.array2ascii(self.array))
        self.assertEqual(self.ascii, gj2ascii.array2ascii(self.np_array))

    def test_roundhouse(self):
        self.assertEqual(self.ascii, gj2ascii.array2ascii(gj2ascii.ascii2array(self.ascii)))
        self.assertEqual(self.array, gj2ascii.ascii2array(gj2ascii.array2ascii(self.array)))


class TestStyle(unittest.TestCase):

    def test_style(self):

        array = [['0', '0', '0', '1', '0'],
                 [' ', ' ', '2', '0', '1'],
                 ['1', '1', '2', '1', '3']]
        colormap = {
            ' ': 'black',
            '0': 'blue',
            '1': 'yellow',
            '2': 'white',
            '3': 'red'
        }
        expected = []
        for row in array:
            o_row = []
            for char in row:
                o_row.append(gj2ascii.ANSI_COLOR_MAP[colormap[char]] + (char * 2) + gj2ascii._core._ANSI_RESET)
            expected.append(''.join(o_row))
        expected = os.linesep.join(expected)
        self.assertEqual(expected, gj2ascii.style(gj2ascii.array2ascii(array), colormap=colormap))
