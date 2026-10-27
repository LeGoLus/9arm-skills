"""Unit tests for the pure helpers. Run: <venv>/bin/python -m pytest -q  (or python3 this_file)"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from print_upscale import crop_box_for_aspect, parse_vtracer_svg, trace_size  # noqa: E402


class CropTests(unittest.TestCase):
    def test_a_series_to_100x140_trims_height_only(self):
        # A-series 7020x9924 -> 1:1.4 keeps full width, trims 96 px split top/bottom
        self.assertEqual(crop_box_for_aspect(7020, 9924, 100, 140), (0, 48, 7020, 9876))

    def test_too_wide_trims_sides(self):
        l, t, r, b = crop_box_for_aspect(2000, 1000, 1, 1)
        self.assertEqual((r - l, b - t), (1000, 1000))
        self.assertEqual(l, 500)

    def test_exact_aspect_is_untouched(self):
        self.assertEqual(crop_box_for_aspect(1000, 1400, 100, 140), (0, 0, 1000, 1400))


class TraceSizeTests(unittest.TestCase):
    def test_caps_long_side(self):
        self.assertEqual(trace_size(7020, 9828), (4914, 6880))

    def test_small_image_not_upscaled(self):
        self.assertEqual(trace_size(800, 600), (800, 600))


class SvgParseTests(unittest.TestCase):
    SVG = ('<path d="M0 0 C1 2 3 4 5 6 L7 8 9 10 Z M1 1 L2 2 Z " fill="#A0B0C0" '
           'transform="translate(3,4)"/>')

    def test_ops_and_implicit_lineto(self):
        (fill, tx, ty, ops), = list(parse_vtracer_svg(self.SVG))
        self.assertEqual((fill, tx, ty), ("#A0B0C0", 3.0, 4.0))
        self.assertEqual(ops, [("M", 0.0, 0.0), ("C", 1.0, 2.0, 3.0, 4.0, 5.0, 6.0),
                               ("L", 7.0, 8.0), ("L", 9.0, 10.0), ("Z",),
                               ("M", 1.0, 1.0), ("L", 2.0, 2.0), ("Z",)])

    def test_negative_and_decimal_numbers(self):
        svg = '<path d="M-1.5 2.25 L-3 -4 Z" fill="#000000" transform="translate(0,0)"/>'
        (_, _, _, ops), = list(parse_vtracer_svg(svg))
        self.assertEqual(ops[:2], [("M", -1.5, 2.25), ("L", -3.0, -4.0)])


if __name__ == "__main__":
    unittest.main()
