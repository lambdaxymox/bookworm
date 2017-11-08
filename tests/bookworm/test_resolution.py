import unittest

from bookworm.resolution import Resolution, ResolutionUnits


class TestResolution(unittest.TestCase):

    def test_make_resolution_should_accept_correct_input(self):
        """
        The ``Resolution`` function ``make`` should accept correct input
        for object creation.
        """
        resolution_val = 600
        resolution_units = 'PixelsPerInch'
        resolution = Resolution.make(resolution_val, resolution_units)

        self.assertIsInstance(resolution, Resolution)
        self.assertEqual(resolution.units, ResolutionUnits.PixelsPerInch)


class TestResolutionFactoryMethod(unittest.TestCase):

    def test_make_resolution_should_only_accept_certain_units(self):
        """
        The ``Resolution`` factory method ``make`` should reject any value
        in units that do not match one of the ones allowed by the 
        ``Resolution`` class.
        """
        resolution_val = 600
        resolution_units = 'Potato'

        self.assertRaises(ValueError, Resolution.make, resolution_val, resolution_units)


    def test_make_resolution_should_reject_negative_values(self):
        """
        The factory method ``make`` should reject negative values for a resolution. Negative or zero
        dots per inch does not make sense.
        """
        resolution_val = -600
        resolution_units = 'PixelsPerInch'

        self.assertRaises(ValueError, Resolution.make, resolution_val, resolution_units)


    def test_make_resolution_should_reject_non_integer_values(self):
        """
        The factory method ``make`` should reject fractional values of inputs.
        """
        resolution_val = 600.1
        resolution_units = 'PixelsPerInch'

        self.assertRaises(TypeError, Resolution.make, resolution_val, resolution_units)

