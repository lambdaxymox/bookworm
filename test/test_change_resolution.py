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

        action = change_resolution.change_page_resolution(resolution, source_file)

        self.assertIsInstance(action, change_resolution.ChangeResolution)
        self.assertEqual(action.source, target_file)


    def test_process_args(self):
        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample.tiff'
        resolution_val = 600
        arg_dict = {'input': source_file, 'output': target_file, 'resolution': resolution_val}

        action = change_resolution.process_args(arg_dict)

        self.assertIsInstance(action, change_resolution.ChangeResolution)
        self.assertEqual(action.source, target_file)
