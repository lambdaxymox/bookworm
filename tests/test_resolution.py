import unittest
from bookworm.resolution import Resolution


class TestResolution(unittest.TestCase):

    def test_make_resolution_should_only_accept_certain_units(self):
        resolution_val = 600
        resolution_units = 'Potato'

        self.assertRaises(ValueError, Resolution.make_resolution, resolution_val, resolution_units)


    def test_make_resolution_should_reject_negative_values(self):
        resolution_val = -600
        resolution_units = 'PixelsPerInch'

        self.assertRaises(ValueError, Resolution.make_resolution, resolution_val, resolution_units)

    def test_make_resolution_should_reject_non_integer_values(self):
        resolution_val = 600.1
        resolution_units = 'PixelsPerInch'

        self.assertRaises(TypeError, Resolution.make_resolution, resolution_val, resolution_units)

