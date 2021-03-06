"""
Unittests for gj2ascii
"""


import os


# Expected output, file paths, etc. required for tests


def compare_ascii(out1, out2):
    # Zip over two blocks of text and compare each pair of lines
    for o1_line, o2_line in zip(out1.rstrip().splitlines(), out2.rstrip().splitlines()):
        if o1_line.rstrip() != o2_line.rstrip():
            return False
    return True


POLY_FILE = os.path.join('sample-data', 'polygons.geojson')
LINE_FILE = os.path.join('sample-data', 'lines.geojson')
POINT_FILE = os.path.join('sample-data', 'points.geojson')
SINGLE_FEATURE_WV_FILE = os.path.join('sample-data', 'single-feature-WV.geojson')
MULTILAYER_FILE = os.path.join('sample-data', 'multilayer-polygon-line')
SMALL_AOI_POLY_LINE_FILE = os.path.join('sample-data', 'small-aoi-polygon-line.geojson')


EXPECTED_POLYGON_40_WIDE = """
. + . . . . . . . . . . . + . . . . . .
. + + + . . . . . . . . . . . . . . . .
. . . + . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . + . . . . . .
. . . . . . . . . + . . . . . . . . . .
. . . . . . . . . + + . . . . . . . . .
. . . . . . . . . + + + + . . . . . . .
. . . . . . . . . . + + + + . . . . . .
. . . . . . . . . . . + + + . . . . + .
+ + + . . . . . . . . . + + . . . + + +
+ + + + . . . . . . . . . . . . + + + +
. . + . . . . . . + . . . . . . . + + .
. . . . . . . . + + . . . . . . . . + .
. . . . . . . + + + . . . . . . . . + .
. . . . . . + + + + . . . . . . . . . .
. . . . . . + + + + . . . . . . . . . .
. . . . . . . . + + . . . . . . . . . .
"""


EXPECTED_LINE_40_WIDE = """
. . . . . . . . + + + + + + + + + + . .
+ + + + + + + + + . . . . . . . . . . .
+ + . . . . . . . . . . . . . . . . . .
. + + . . . . . . . . . . . . . . . . .
. . + + . . . . . . . . . . . . . . . .
. . . + + + . . . . . . . . . . . . . .
. . . . . + + . . . . . . . . . . . . .
. . . . . . + + . . . . . . . . . . . .
. . . . . . . + + . . . . . . . . . . .
. . . . . . . . + + + . . . . . . . . .
. . . . . . . . . . + + . . . . . . . .
. . . . . . . . . . + . . . . . . . . .
. . . . . . . . . + + . . . . . . . . .
. . . . . . . . + + . . . . . . . . . .
. . . . . . . . + . . . . . . . . . . .
. . . . . . . + + . . . . . . . . . . .
. . . . . . + + . . . . . . . . . . . .
. . . . . + + . . . . . . . . . . . . .
. . . . . + . . . . . . . . . . . . . .
. . . . + + . . . . . . . . . . . . . .
. . . + + . . . . . . . . . . . . . . .
. . . + . . . . . . . . . . . . . . . .
. . + + . . . . . . . . . . . . . . . .
. + + . . . . . . . . . . . . . . . . .
. + . . . . . . . . + . . . . . . . . .
. + + . . . . . . . + + . . . . . . . .
. . + . . . . . . . + + + . . . . . . .
. . + + . . . . . . + . + + . . . . . .
. . . + + . . . . . + . . + + . . . . .
. . . . + + . . . . + . . . + + . . . .
. . . . . + + . . . + . . . . + + . . .
. . . . . . + + . . + . . . . . + + . .
. . . . . . . + + . + . . . . . . + + .
. . . . . . . . + + + . . . . . . . + +

+ . . . . . . . . . . . . . . . . . . .
+ . . . . . . . . . . . . . . . . . . .
+ + . . . . . . . . . . . . . . . . . .
. + . . . . . . . . . . . . . . . . . .
. + . . . . . . . . . . . . . . . . . .
. + + . . . . . . . . . . . . . . . . .
. . + . . . . . . . . . . . . . . . . .
. . + . . . . . . . . . . . . . . . . .
. . + + . . . . . . . . . . . . . . . .
. . . + . . . . . . . . . . . . . . . .
. . . + . . . . . . . . . . . . . . . .
. . . + + . . . . . . . . . . . . . . .
. . . . + . . . . . . . . . . . . . . .
. . . . + + . . . . . . . . . . . . . .
. . . . . + . . . . . . . . . . . . . .
. . . . . + . . . . . . . . . . . . . .
. . . . . + + . . . . . . . . . . . . .
. . . . . . + . . . . . . . . . . . . .
. . . . . . + . . . . . . . . . . . . .
. . . . . . + + . . . . . . . . . . . .
. . . . . . . + . . . . . . . . . . . .
. . . . . . . + . . . . . . . . . . . .
. . . . . . . + + . . . . . . . . . . .
. . . . . . . . + . . . . . . . . . . .
. . . . . . . . + + . . . . . . . . . .
. . . . . . . . . + . . . . . . . . . .
. . . . . . . . . + . . . . . . . . . .
. . . . . . . . . + + . . . . . . . . .
. . . . . . . . . . + . . . . . . . . .
. . . . . . . . . . + . . . . . . . . .
. . . . . . . . . . + + . . . . . . . .
. . . . . . . . . . . + . . . . . . . .
. . . . . . . . . . . + . . . . . . . .
. . . . . . . . . . . + + . . . . . . .
. . . . . . . . . . . . + . . . . . . .
. . . . . . . . . . . . + . . . . . . .
. . . . . . . . . . . . + + . . . . . .
. . . . . . . . . . . . . + . . . . . .
. . . . . . . . . . . . . + + . . . . .
. . . . . . . . . . . . . . + . . . . .
. . . . . . . . . . . . . . + . . . . .
. . . . . . . . . . . . . . + + . . . .
. . . . . . . . . . . . . . . + . . . .
. . . . . . . . . . . . . . . + . . . .
. . . . . . . . . . . . . . . + + . . .
. . . . . . . . . . . . . . . . + . . .
. . . . . . . . . . . . . . . . + . . .
. . . . . . . . . . . . . . . . + + . .
. . . . . . . . . . . . . . . . . + . .
. . . . . . . . . . . . . . . . . + + .
. . . . . . . . . . . . . . . . . . + .
. . . . . . . . . . . . . . . . . . + .
. . . . . . . . . . . . . . . . . . + +
. . . . . . . . . . . . . . . . . . . +
. . . . . . . . . . . . . . . . . . . +

+ + + + + + + + + + + + + + + + + + + +


""".rstrip()


EXPECTED_ALL_PROPERTIES_OUTPUT = """
+----------+----------------+
| STATEFP  |             54 |
| COUNTYFP |            001 |
| COUNTYNS |       01696996 |
| GEOID    |          54001 |
| NAME     |        Barbour |
| NAMELSAD | Barbour County |
| LSAD     |             06 |
| CLASSFP  |             H1 |
| MTFCC    |          G4020 |
| CSAFP    |           None |
| CBSAFP   |           None |
| METDIVFP |           None |
| FUNCSTAT |              A |
| ALAND    |      883338808 |
| AWATER   |        4639183 |
| INTPTLAT |    +39.1397248 |
| INTPTLON |   -079.9969466 |
+----------+----------------+


      + + +   + + +
    + + + + + +
+ + + + + +
+ + + + +
""".rstrip()


EXPECTED_TWO_PROPERTIES_OUTPUT = """
+-------+-----------+
| NAME  |   Barbour |
| ALAND | 883338808 |
+-------+-----------+
* * * * * * * * * *
* * * * * * * * * *
* * * + + + * + + +
* * + + + + + + * *
+ + + + + + * * * *
+ + + + + * * * * *

"""


EXPECTED_STACKED = """
. + . . . . . . . . . . . + . . . . . .
. + + + . . . . . . . . . . . . . . . .
. . 8 8 8 8 8 8 8 . . . . 8 . . . . . .
. . . 8 . . . . . . . . . 8 . . . . . .
. . . . 8 . . . . + . . . . 8 . . . . .
. . . . . 8 . . . + + . . . 8 . . . . .
. . . . . . 8 . . + + + + . 8 . . . . .
. . . . . 8 . . . . + + + + . 8 . . . .
. . . . 8 . . . . . . 8 8 8 . 8 . . + .
+ + + . 8 . . . 8 8 8 . + + . . 8 + + +
+ + + 8 . . . . . . . . . . . . 8 + + +
. . 8 . . . 8 . . + . . . . . . 8 + + .
. . . 8 . . 8 8 + + . . . . . . . 8 + .
. . . . 8 . 8 + 8 + . . . . . . . 8 + .
. . . . 8 8 + + 8 + . . . . . . . . . .
. . . . . 8 + + + 8 . . . . . . . . . .
. . . . . . . . + + . . . . . . . . . .
"""


EXPECTED_STACK_PERCENT_ALL = """
  1                       1
  1 1 1
    0 1 0 0 0 0 0         0
      0                   1
        0         1         0
          0       1 1       0
            0     1 1 1 1   0
          0         1 1 1 1   0
        0             1 1 1   0     1
1 1 1   0       0 0 0   1 1     0 1 1 1
1 1 1 1                         1 1 1 1
    1       0     1             0 1 1
      0     0 0 1 1               0 1
        0   0 1 1 1               0 1
        0 0 1 1 1 1
          0 1 1 1 1
                1 1

"""


EXPECTED_BBOX_POLY = """
                                + + + +
                                  + + +
                                    + +
                                      +
+ +
+ + +
+ + +
+ +
+ +                         +
                          + +
                        + + +
                      + + + +
                    + + + + +
                  + + + + + +
                + + + + + + +

"""
