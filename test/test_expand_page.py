import unittest
import os
import expand_page

class TestExpandPageWithFill(unittest.TestCase):

    def test_expand_page_with_fill(self):

        source_file = 'sample/sample1.tiff'
        target_file = 'sample/sample1.bookworm.tiff'
        width = 2160
        height = 3060

        action = expand_page.expand_page_with_fill(width, height, source_file)

        correct_subcommand = [
                'convert', '-extent {}x{}'.format(width, height), '-background white', 
                '-gravity Center', '\"'+source_file+'\"', '\"'+target_file+'\"'
            ]

        self.assertEqual(action.as_python_subprocess(), correct_subcommand)


    def test_process_args(self):

        source     = 'sample/sample.tiff'
        target     = source
        width      = 2160
        height     = 3060
        dimensions = (width, height)
        arg_dict = {'input': source, 'dimensions': dimensions}

        action = expand_page.process_args(arg_dict)

        # No exception occurred.
        self.assertIsInstance(action, expand_page.ExpandPageWithFill)
        self.assertEqual(action.width, width)
        self.assertEqual(action.height, height)
        self.assertEqual(action.source, source)


    def test_process_args_should_reject_bad_dimensions(self):

        source     = 'sample/sample.tiff'
        target     = source
        width      = 2160
        height     = "Potato"
        dimensions = (width, height)
        arg_dict = {'input': source, 'dimensions': dimensions}

        action = None

        try:
            action = expand_page.process_args(arg_dict)
        except TypeError as e:
            # Successful trap.
            self.assertIsInstance(e, TypeError)

        # An error should occur from malformed input.
        self.assertNotEqual(type(action), expand_page.ExpandPageWithFill)