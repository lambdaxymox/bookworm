import unittest
import bookworm.resample_page as resample_page
import os
import os.path

from bookworm.resolution import Resolution


class TestResamplePage(unittest.TestCase):

    def test_resample_page(self):
        """
        The factory method should generate valid instances of ``ResamplePage``.
        """
        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample.tiff'
        resolution_val = 600
        unit_str = 'PixelsPerInch'

        resolution = Resolution.make(resolution_val, unit_str)
        try:
            action = resample_page.make(resolution, source_file, target_file)
        except ValueError as e:
            self.fail("An error should not have occurred here.")

        self.assertIsInstance(action, resample_page.ResamplePage)


class TestResamplePageProcessArgs(unittest.TestCase):

    def test_process_args(self):
        """
        The argument process should create a valid ``ResamplePage``
        given valid input values.
        """
        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample.tiff'
        resolution_val = 600
        unit_str = 'PixelsPerInch'
        arg_dict = {
            'input': source_file,
            'output': target_file,
            'resolution': resolution_val,
            'units': unit_str
        }

        try:
            action = resample_page.process_args(arg_dict)
        except ValueError as e:
            self.fail("An error should not have occurred here.")

        self.assertIsInstance(action, resample_page.ResamplePage)


    def test_process_args_should_reject_zero_resolution(self):
        """
        Given an input resolution value of zero, the argument processor
        should reject it. It is impossible to have a pdf page with a
        resolution of zero.
        """
        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample.tiff'
        resolution_val = 0
        unit_str = 'PixelsPerInch'
        arg_dict = {
            'input': source_file,
            'output': target_file,
            'resolution': resolution_val,
            'units': unit_str
        }

        with self.assertRaises(ValueError):
            resample_page.process_args(arg_dict)


    def test_process_args_should_reject_negative_resolution(self):
        """
        Given a negative input resolution value, the argument processor
        should not accept it. Having a negative resolution value makes no
        sense.
        """
        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample.tiff'
        resolution_val = -300
        unit_str = 'PixelsPerInch'
        arg_dict = {
            'input': source_file,
            'output': target_file,
            'resolution': resolution_val,
            'units': unit_str
        }

        with self.assertRaises(ValueError):
            resample_page.process_args(arg_dict)


    def test_process_args_should_reject_noninteger_resolutions(self):
        """
        The argument processor only supports positive integer resolutions.
        """
        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample.tiff'
        resolution_val = 300.1
        unit_str = 'PixelsPerInch'
        arg_dict = {
            'input': source_file,
            'output': target_file,
            'resolution': resolution_val,
            'units': unit_str
        }

        with self.assertRaises(TypeError):
            resample_page.process_args(arg_dict)


    def test_process_args_should_reject_missing_units(self):
        """
        The argument processor should not accept an input resolution
        that has missing units.
        """
        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample.tiff'
        resolution_val = 300
        arg_dict = {
            'input': source_file,
            'output': target_file,
            'resolution': resolution_val
        }

        with self.assertRaises(KeyError):
            resample_page.process_args(arg_dict)


class TestRunner(unittest.TestCase):

    def test_resample_page_runner(self):
        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample2.tiff'
        resolution = 600
        arg_dict = {
            'input': source_file,
            'output': target_file,
            'resolution': resolution,
            'units': 'PixelsPerInch'
        }
        action = resample_page.process_args(arg_dict)

        resample_page.Runner.setup(action)
        resample_page.Runner.execute(action)
        target_file_exists = os.path.exists(action.target_file)
        os.remove(target_file)

        self.assertTrue(target_file_exists)

