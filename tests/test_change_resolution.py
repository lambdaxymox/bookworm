import unittest
import bookworm.change_resolution as change_resolution
import os

from bookworm.resolution import Resolution


class TestChangeResolution(unittest.TestCase):

    def test_change_resolution(self):
        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample.tiff'
        resolution_val = 600
        unit_str = 'PixelsPerInch'
        resolution = Resolution.make(resolution_val, unit_str)

        try:
            action = change_resolution.change_page_resolution(resolution, source_file)
        except ValueError as e:
            self.fail()

        self.assertIsInstance(action, change_resolution.ChangeResolution)
        self.assertEqual(action.source, target_file)


class TestChangeResolutionProcessArgs(unittest.TestCase):
    
    def test_process_args(self):
        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample.tiff'
        resolution_val = 600
        arg_dict = {
            'input': source_file,
            'output': target_file,
            'resolution': resolution_val,
            'units': 'PixelsPerInch'
        }

        try:
            action = change_resolution.process_args(arg_dict)
        except ValueError as e:
            self.fail("An error should not have occurred here.")

        self.assertIsInstance(action, change_resolution.ChangeResolution)
        self.assertEqual(action.source, target_file)


    def test_process_args_should_reject_missing_units(self):
        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample.tiff'
        resolution_val = 600
        arg_dict = {
            'input': source_file,
            'output': target_file,
            'resolution': resolution_val
        }

        with self.assertRaises(KeyError):
            change_resolution.process_args(arg_dict)


    def test_process_args_should_reject_noninteger_values(self):
        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample.tiff'
        resolution_val = "Potato"
        arg_dict = {
            'input': source_file,
            'output': target_file,
            'resolution': resolution_val,
            'units': 'PixelsPerInch'
        }

        with self.assertRaises(TypeError):
            change_resolution.process_args(arg_dict)


    def test_process_args_should_reject_nonpositive_resolution_values(self):
        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample.tiff'
        resolution_val = -600
        arg_dict = {
            'input': source_file,
            'output': target_file,
            'resolution': resolution_val,
            'units': 'PixelsPerInch'
        }

        with self.assertRaises(ValueError):
            change_resolution.process_args(arg_dict)


    def test_process_args_should_reject_resolution_value_of_zero(self):
        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample.tiff'
        resolution_val = 0
        arg_dict = {
            'input': source_file,
            'output': target_file,
            'resolution': resolution_val,
            'units': 'PixelsPerInch'
        }
        
        with self.assertRaises(ValueError):
            change_resolution.process_args(arg_dict)


class TestMultiChangePageResolution(unittest.TestCase):

    def test_multi_page_change_resolution_should_generation_multiple_actions_from_input_directory(self):
        source_dir = 'sample/test_tiffs/'
        source_files = list(map(lambda f: os.path.join(source_dir, f), os.listdir(source_dir)))
        resolution_val = 600
        resolution = Resolution.make(resolution_val, 'PixelsPerInch')
        arg_dict = {
            'input': source_dir,
            'resolution': resolution_val,
            'units': 'PixelsPerInch'
        }

        multi_actions = change_resolution.process_args(arg_dict)
        for action in multi_actions.values():
            self.assertIsInstance(action, change_resolution.ChangeResolution)
            self.assertIsInstance(action.resolution, Resolution)
            self.assertEqual(action.resolution.value, resolution.value)
            self.assertEqual(action.resolution.units, resolution.units)
            self.assertTrue(action.source in source_files)


    def test_process_args_should_reject_non_existent_input_directory(self):
        source = 'sample/directory_doesnotexist/'
        resolution_val = 600
        arg_dict = {
            'input': source,
            'resolution': resolution_val,
            'units': 'PixelsPerInch'
        }
        
        with self.assertRaises(FileNotFoundError):
            change_resolution.process_args(arg_dict)


    def test_process_args_should_reject_nonpositive_integer_resolutions(self):
        source = 'sample/sample_tiffs/'
        resolution_val = -600
        arg_dict = {
            'input': source,
            'resolution': resolution_val,
            'units': 'PixelsPerInch'
        }

        try:
            action = change_resolution.process_args(arg_dict)

            # Action should not have been assigned a value.
            self.fail(f'Negative integer accepted: {action}')
        except TypeError as e:
            self.assertIsInstance(e, TypeError)
        except ValueError as e:
            self.assertIsInstance(e, ValueError)


    def test_process_args_should_reject_fractional_resolution_values(self):
        source = 'sample/sample_tiffs/'
        resolution_val = 600.1
        arg_dict = {
            'input': source,
            'resolution': resolution_val,
            'units': 'PixelsPerInch'
        }

        try:
            action = change_resolution.process_args(arg_dict)

            # Action should not have been assigned a value.
            self.fail(f'Fractional value accepted: {action}')
        except TypeError as e:
            self.assertIsInstance(e, TypeError)
        except ValueError as e:
            self.assertIsInstance(e, ValueError)
            
