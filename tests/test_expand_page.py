import unittest
import os
import bookworm.expand_page as expand_page


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


class TestExpandPageWithFillProcessArgs(unittest.TestCase):

    def test_process_args(self):
        source = 'sample/sample.tiff'
        width = 2160
        height = 3060
        dimensions = (width, height)
        arg_dict = {'input': source, 'dimensions': dimensions}

        action = expand_page.process_args(arg_dict)

        # No exception occurred.
        self.assertIsInstance(action, expand_page.ExpandPageWithFill)
        self.assertEqual(action.width, width)
        self.assertEqual(action.height, height)
        self.assertEqual(action.source, source)


    def test_process_args_should_reject_bad_dimensions(self):
        source = 'sample/sample.tiff'
        width = 2160
        height = "Potato"
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


    def test_process_args_should_reject_non_existent_file(self):
        source = 'sample/sample_doesnotexist.tiff'
        width = 2160
        height = 3060
        dimensions = (width, height)
        arg_dict = {'input': source, 'dimensions': dimensions}

        action = None
        try:
            action = expand_page.process_args(arg_dict)
        except FileNotFoundError as e:
            # An exception should occur.
            self.assertIsInstance(e, FileNotFoundError)

        # Action should not have been assigned a value.
        self.assertIsInstance(action, type(None))


class TestMultipleExpandPages(unittest.TestCase):

    def test_process_args_should_generate_multiple_actions_from_input_directory(self):
        source_dir = 'sample/test_tiffs/'
        source_files = list(map(lambda f: os.path.join(source_dir, f), os.listdir(source_dir)))
        width = 2160
        height = 3060
        dimensions = (width, height)
        arg_dict = {'input': source_dir, 'dimensions': dimensions}

        multi_actions = expand_page.process_args(arg_dict)

        for action in multi_actions.values():
            self.assertIsInstance(action, expand_page.ExpandPageWithFill)
            self.assertEqual(action.width, width)
            self.assertEqual(action.height, height)
            self.assertTrue(action.source in source_files)


    def test_process_args_should_reject_non_existent_input_directory(self):
        source = 'sample/directory_doesnotexist/'
        width = 2160
        height = 3060
        dimensions = (width, height)
        arg_dict = {'input': source, 'dimensions': dimensions}

        action = None
        try:
            action = expand_page.process_args(arg_dict)
        except FileNotFoundError as e:
            # An exception should occur.
            self.assertIsInstance(e, FileNotFoundError)

        # Action should not have been assigned a value.
        self.assertIsInstance(action, type(None))

