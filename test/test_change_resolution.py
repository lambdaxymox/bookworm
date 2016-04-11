import unittest
import change_resolution
import command

class TestChangeResolution(unittest.TestCase):

    def test_change_resolution(self):

        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample.tiff'
        resolution_val = 600
        unit_str = 'PixelsPerInch'

        resolution = command.make_resolution(resolution_val, unit_str)
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

    pass