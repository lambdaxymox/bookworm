import unittest
import bookworm.change_resolution as change_resolution
import os

from bookworm.resolution import Resolution


class TestChangeResolution(unittest.TestCase):

    def test_change_resolution(self):
        """
        We should be able to create a page action that has the correct type.
        """
        source_file = 'sample/sample.tiff'
        resolution_val = 600
        unit_str = 'PixelsPerInch'
        resolution = Resolution.make(resolution_val, unit_str)

        try:
            action = change_resolution.make(resolution, source_file)
        except ValueError as e:
            self.fail()

        self.assertIsInstance(action, change_resolution.ChangeResolution)
        self.assertNotEqual(action.target_file, action.source_file)


class TestChangeResolutionProcessArgs(unittest.TestCase):
    
    def test_process_args(self):
        """
        The argument processor should correctly create a ``ChangeResolution``
        action under conditions where there is a positive resolution value when
        units are given.
        """
        source_file = 'sample/sample.tiff'
        target_path = 'sample/'
        resolution_val = 600
        arg_dict = {
            'input': source_file,
            'output': target_path,
            'resolution': resolution_val,
            'units': 'PixelsPerInch'
        }

        try:
            action = change_resolution.process_args(arg_dict)
        except ValueError as e:
            self.fail("An error should not have occurred here.")

        self.assertIsInstance(action, change_resolution.ChangeResolution)
        self.assertNotEqual(action.source_file, action.target_file)


    def test_process_args_should_reject_missing_units(self):
        """
        The argument processor should not create a ``ChangeResolution`` action
        if the input resolution desired has no units.
        """
        source_file = 'sample/sample.tiff'
        target_path = 'sample/'
        resolution_val = 600
        arg_dict = {
            'input': source_file,
            'output': target_path,
            'resolution': resolution_val
        }

        with self.assertRaises(KeyError):
            change_resolution.process_args(arg_dict)


    def test_process_args_should_reject_noninteger_values(self):
        """
        The argument processor should not accept a noninteger input value for
        the image resolution.
        """
        source_file = 'sample/sample.tiff'
        target_path = 'sample/'
        resolution_val = "Potato"
        arg_dict = {
            'input': source_file,
            'output': target_path,
            'resolution': resolution_val,
            'units': 'PixelsPerInch'
        }

        with self.assertRaises(TypeError):
            change_resolution.process_args(arg_dict)


    def test_process_args_should_reject_nonpositive_resolution_values(self):
        """
        The argument processor should not accept a negative input value for
        the image resolution.
        """
        source_file = 'sample/sample.tiff'
        target_path = 'sample/'
        resolution_val = -600
        arg_dict = {
            'input': source_file,
            'output': target_path,
            'resolution': resolution_val,
            'units': 'PixelsPerInch'
        }

        with self.assertRaises(ValueError):
            change_resolution.process_args(arg_dict)


    def test_process_args_should_reject_resolution_value_of_zero(self):
        """
        The argument processor should not accept zero as an input value for
        the image resolution.
        """
        source_file = 'sample/sample.tiff'
        target_path = 'sample/'
        resolution_val = 0
        arg_dict = {
            'input': source_file,
            'output': target_path,
            'resolution': resolution_val,
            'units': 'PixelsPerInch'
        }
        
        with self.assertRaises(ValueError):
            change_resolution.process_args(arg_dict)


class TestChangeResolutionRunner(unittest.TestCase):

    def test_change_resolution_runner_process(self):
        source_file = 'sample/sample.tiff'
        target_path = 'sample/'
        resolution_val = 600
        arg_dict = {
            'input': source_file,
            'output': target_path,
            'resolution': resolution_val,
            'units': 'PixelsPerInch'
        }
        action = change_resolution.process_args(arg_dict)

        try:
            change_resolution.Runner.setup(action)
            change_resolution.Runner.execute(action)
        except FileNotFoundError as e:
            change_resolution.Runner.cleanup(action)
            self.fail()
        else:
            change_resolution.Runner.cleanup(action)


    def test_runner_should_fail_if_source_does_not_exist(self):
        source_file = 'sample/doesnotexist.tiff'
        target_path = 'sample/'
        resolution_val = 600
        arg_dict = {
            'input': source_file,
            'output': target_path,
            'resolution': resolution_val,
            'units': 'PixelsPerInch'
        }

        with self.assertRaises(FileNotFoundError):
            action = change_resolution.process_args(arg_dict)
            change_resolution.Runner.setup(action)


class TestMultiChangePageResolution(unittest.TestCase):

    def test_multi_page_change_resolution_should_generate_multiple_actions_from_input_directory(self):
        """
        Given a valid input directory with zero or more files in it, a multiple
        page change resolution action argument processor should correctly
        every valid input image and group them together into one action.
        """
        source_path = 'sample/test_tiffs/'
        source_files = list(map(lambda f: os.path.join(source_path, f), os.listdir(source_path)))
        resolution_val = 600
        resolution = Resolution.make(resolution_val, 'PixelsPerInch')
        arg_dict = {
            'input': source_path,
            'resolution': resolution_val,
            'units': 'PixelsPerInch'
        }

        multi_actions = change_resolution.process_args(arg_dict)
        for action in multi_actions.values():
            self.assertIsInstance(action, change_resolution.ChangeResolution)
            self.assertIsInstance(action.resolution, Resolution)
            self.assertEqual(action.resolution.value, resolution.value)
            self.assertEqual(action.resolution.units, resolution.units)
            self.assertTrue(action.source_file in source_files)


    def test_process_args_should_reject_non_existent_input_directory(self):
        """
        The arument processor should not accept an input directory that does
        not exist. Surely it is impossible to read a nonexistent input.
        """
        source_path = 'sample/directory_doesnotexist/'
        resolution_val = 600
        arg_dict = {
            'input': source_path,
            'resolution': resolution_val,
            'units': 'PixelsPerInch'
        }
        
        with self.assertRaises(FileNotFoundError):
            change_resolution.process_args(arg_dict)


    def test_process_args_should_reject_nonpositive_integer_resolutions(self):
        """
        Thr argument processor should reject negative and zero values for
        the new resolution for the image. It does not make sense to have 
        negative pixels per inch.
        """
        source_path = 'sample/sample_tiffs/'
        resolution_val = -600
        arg_dict = {
            'input': source_path,
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
        """
        The ``ChangeResolution`` action's argument processor should not accept
        fractional resolution values.
        """
        source_path = 'sample/sample_tiffs/'
        resolution_val = 600.1
        arg_dict = {
            'input': source_path,
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
            
