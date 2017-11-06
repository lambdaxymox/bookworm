import unittest
import bookworm.resample_page as resample_page
import bookworm.util as util
import os

from bookworm.resolution import Resolution


class TestResamplePage(unittest.TestCase):

    def test_resample_page(self):
        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample.tiff'
        resolution_val = 600
        unit_str = 'PixelsPerInch'

        resolution = Resolution.make(resolution_val, unit_str)
        try:
            action = resample_page.resample_page(resolution, source_file)
        except ValueError as e:
            self.fail("An error should not have occurred here.")

        self.assertIsInstance(action, resample_page.ResamplePage)


class TestResamplePageProcessArgs(unittest.TestCase):

    def test_process_args(self):
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
