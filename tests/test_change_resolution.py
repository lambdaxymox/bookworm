import unittest
import bookworm.change_resolution as change_resolution
import bookworm.util as util
import os

from bookworm.resolution import Resolution


class TestChangeResolution(unittest.TestCase):

    def test_change_resolution(self):
        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample.tiff'
        resolution_val = 600
        unit_str = 'PixelsPerInch'

        resolution = util.make_resolution(resolution_val, unit_str)
        try:
            action = change_resolution.change_page_resolution(resolution, source_file)
        except ValueError as e:
            self.fail()

        self.assertIsInstance(action, change_resolution.ChangeResolution)
        self.assertEqual(action.source, target_file)


    def test_process_args(self):
        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample.tiff'
        resolution_val = 600
        arg_dict = {'input': source_file, 'output': target_file, 'resolution': resolution_val}

        try:
            action = change_resolution.process_args(arg_dict)
        except ValueError as e:
            self.fail("An error should not have occurred here.")

        self.assertIsInstance(action, change_resolution.ChangeResolution)
        self.assertEqual(action.source, target_file)


    def test_process_args_should_reject_bad_resolution_values(self):
        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample.tiff'
        resolution_val = "Potato"
        arg_dict = {'input': source_file, 'output': target_file, 'resolution': resolution_val}

        action = None

        try:
            action = change_resolution.process_args(arg_dict)
        except TypeError as e:
            # Successful trap.
            self.assertIsInstance(e, TypeError)

        # An error should occur from malformed input.
        self.assertNotEqual(type(action), change_resolution.ChangeResolution)


    def test_process_args_should_reject_nonpositive_resolution_values(self):
        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample.tiff'
        resolution_val = -600
        arg_dict = {'input': source_file, 'output': target_file, 'resolution': resolution_val}

        action = None

        try:
            action = change_resolution.process_args(arg_dict)
        except ValueError as e:
            self.assertIsInstance(action, type(None))

        # An error should occur from malformed input.
        self.assertNotEqual(type(action), change_resolution.ChangeResolution)
        
        action = None
        resolution_val = 0
        arg_dict = {'input': source_file, 'output': target_file, 'resolution': resolution_val}
        
        try:
            action = change_resolution.process_args(arg_dict)
        except ValueError as e:
            self.assertIsInstance(action, type(None))

        # An error should occur from malformed input.
        self.assertNotEqual(type(action), change_resolution.ChangeResolution)


class TestMultiChangePageResolution(unittest.TestCase):

    def test_multi_page_change_resolution_should_generation_multiple_actions_from_input_directory(self):
        source_dir = 'sample/test_tiffs/'
        source_files = list(map(lambda f: os.path.join(source_dir, f), os.listdir(source_dir)))
        resolution_val = 600
        resolution = util.make_resolution(resolution_val, 'PixelsPerInch')

        arg_dict = {'input': source_dir, 'resolution': resolution_val}

        multi_actions = change_resolution.process_args(arg_dict)

        for action in multi_actions.values():
            self.assertIsInstance(action, change_resolution.ChangeResolution)
            self.assertIsInstance(action.resolution, Resolution)
            self.assertEqual(action.resolution.resolution, resolution.resolution)
            self.assertEqual(action.resolution.units, resolution.units)
            self.assertTrue(action.source in source_files)


    def test_process_args_should_reject_non_existent_input_directory(self):
        source = 'sample/directory_doesnotexist/'
        resolution_val = 600
        arg_dict = {'input': source, 'resolution': resolution_val }
        action = None

        try:
            action = change_resolution.process_args(arg_dict)
        except FileNotFoundError as e:
            # An exception should occur.
            self.assertIsInstance(e, FileNotFoundError)

        # Action should not have been assigned a value.
        self.assertIsInstance(action, type(None))


    def test_process_args_should_reject_nonnnegative_integer_resolutions(self):
        source = 'sample/sample_tiffs/'
        resolution_val = -600
        
        try:
            arg_dict = {'input': source, 'resolution': resolution_val }
            action = change_resolution.process_args(arg_dict)

            # Action should not have been assigned a value.
            self.fail('Negative integer accepted for resolution value.')
        except TypeError as e:
            self.assertIsInstance(e, TypeError)
        except ValueError as e:
            self.assertIsInstance(e, ValueError)

        resolution_val = 600.1

        try:
            arg_dict = {'input': source, 'resolution': resolution_val}
            action = change_resolution.process_args(arg_dict)

            # Action should not have been assigned a value.
            self.fail('Fractional value accepted for resolution value.')
        except TypeError as e:
            self.assertIsInstance(e, TypeError)
        except ValueError as e:
            self.assertIsInstance(e, ValueError)
            
