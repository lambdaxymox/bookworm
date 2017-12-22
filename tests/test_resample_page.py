import pytest
import unittest
import bookworm.resample_page as resample_page
import os
import os.path

from bookworm.resolution import Resolution
from collections import namedtuple


class TestResamplePage(unittest.TestCase):

    def test_resample_page(self):
        """
        The factory method should generate valid instances of ``ResamplePage``.
        """
        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample.tiff'
        resolution_val = 300
        unit_str = 'PixelsPerInch'
        
        resolution = Resolution.make(resolution_val, unit_str)
        action = resample_page.make(resolution, source_file, target_file)

        self.assertIsInstance(action, resample_page.ResamplePage)


class TestResamplePageProcessArgs(unittest.TestCase):

    def setUp(self):
        self.arg_dict = dict(
            input =  'sample/sample.tiff',
            output = 'sample/sample.tiff',
            units = 'PixelsPerInch'
        )

    def use_resolution_val(self, resolution_val):
        self.arg_dict['resolution'] = resolution_val

    def test_process_args(self):
        """
        The argument process should create a valid ``ResamplePage``
        given valid input values.
        """
        self.use_resolution_val(300)
        action = resample_page.process_args(self.arg_dict)

        self.assertIsInstance(action, resample_page.ResamplePage)


    def test_process_args_should_reject_zero_resolution(self):
        """
        Given an input resolution value of zero, the argument processor
        should reject it. It is impossible to have a pdf page with a
        resolution of zero.
        """
        self.use_resolution_val(0)
        with self.assertRaises(ValueError):
            resample_page.process_args(self.arg_dict)


    def test_process_args_should_reject_negative_resolution(self):
        """
        Given a negative input resolution value, the argument processor
        should not accept it. Having a negative resolution value makes no
        sense.
        """
        self.use_resolution_val(-300)
        with self.assertRaises(ValueError):
            resample_page.process_args(self.arg_dict)


    def test_process_args_should_reject_noninteger_resolutions(self):
        """
        The argument processor only supports positive integer resolutions.
        """
        self.use_resolution_val(300.1)
        with self.assertRaises(TypeError):
            resample_page.process_args(self.arg_dict)


class TestProcessArgsWithMissingResolutionUnits(unittest.TestCase):

    def setUp(self):
        self.arg_dict = dict(
            input = 'sample/sample.tiff',
            output = 'sample/sample.tiff',
            resolution = 300
        )

    def test_process_args_should_reject_missing_units(self):
        """
        The argument processor should not accept an input resolution
        that has missing units.
        """
        with self.assertRaises(KeyError):
            resample_page.process_args(self.arg_dict)


class TestRunner:

    Data = namedtuple('Data', 'arg_dict action')

    @pytest.fixture
    def fixture(self):
        arg_dict = dict(
            input = 'sample/sample.tiff',
            output = 'sample/sample2.tiff',
            resolution = 300,
            units = 'PixelsPerInch'
        )
        action = resample_page.process_args(arg_dict)

        yield self.Data(arg_dict, action)
        os.remove(action.target_file)

    
    def test_resample_page_runner(self, fixture):
        resample_page.Runner.setup(fixture.action)
        resample_page.Runner.execute(fixture.action)

        assert os.path.exists(fixture.action.target_file)

