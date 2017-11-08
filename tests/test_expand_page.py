import unittest
import os
import bookworm.expand_page as expand_page


class TestExpandPageWithFill(unittest.TestCase):

    def test_expand_page_with_fill(self):
        """
        The page action should generate a valid python subprocess 
        or terminal command under normal conditions.
        """
        source_file = 'sample/sample1.tiff'
        target_file = 'sample/sample1.bookworm.tiff'
        width = 2160
        height = 3060
        action = expand_page.make(width, height, source_file)

        self.assertIsInstance(action, expand_page.ExpandPageWithFill)


class TestExpandPageWithFillProcessArgs(unittest.TestCase):

    def test_process_args(self):
        """
        The argument processor should produce a valid instance of
        a page action given valid inputs.
        """
        source_file = 'sample/sample.tiff'
        width = 2160
        height = 3060
        dimensions = (width, height)
        arg_dict = {'input': source_file, 'dimensions': dimensions}

        action = expand_page.process_args(arg_dict)

        # No exception occurred.
        self.assertIsInstance(action, expand_page.ExpandPageWithFill)
        self.assertEqual(action.width, width)
        self.assertEqual(action.height, height)
        self.assertEqual(action.source_file, source_file)


    def test_process_args_should_reject_bad_dimensions(self):
        """
        The new dimensions of the input page should both be integer values.
        You cannot define the notion of width and height by other means in
        terms of pixels.
        """
        source_file = 'sample/sample.tiff'
        width = 2160
        height = "Potato"
        dimensions = (width, height)
        arg_dict = {'input': source_file, 'dimensions': dimensions}

        action = None
        try:
            action = expand_page.process_args(arg_dict)
        except TypeError as e:
            # Successful trap.
            self.assertIsInstance(e, TypeError)

        # An error should occur from malformed input.
        self.assertNotEqual(type(action), expand_page.ExpandPageWithFill)


    ### TODO: a setup action should handle this!!!
    def test_process_args_should_reject_non_existent_file(self):
        """
        The argument processor should only generate a valid input if the
        input file actually exists.
        """
        source_file = 'sample/sample_doesnotexist.tiff'
        width = 2160
        height = 3060
        dimensions = (width, height)
        arg_dict = {'input': source_file, 'dimensions': dimensions}

        with self.assertRaises(FileNotFoundError):
            expand_page.process_args(arg_dict)


class TestMultipleExpandPages(unittest.TestCase):

    def test_process_args_should_generate_multiple_actions_from_input_directory(self):
        """
        If an input directory exists and has multiple tiff files in it, the
        argument processor should find them and pack them together into a
        multiple page action.
        """
        source_path = 'sample/test_tiffs/'
        source_files = list(map(lambda f: os.path.join(source_path, f), os.listdir(source_path)))
        width = 2160
        height = 3060
        dimensions = (width, height)
        arg_dict = {'input': source_path, 'dimensions': dimensions}

        multi_actions = expand_page.process_args(arg_dict)

        for action in multi_actions.values():
            self.assertIsInstance(action, expand_page.ExpandPageWithFill)
            self.assertEqual(action.width, width)
            self.assertEqual(action.height, height)
            self.assertTrue(action.source_file in source_files)


    def test_process_args_should_reject_non_existent_input_directory(self):
        """
        If the input directory does not exist, there is no work to be done.
        """
        source_path = 'sample/directory_doesnotexist/'
        width = 2160
        height = 3060
        dimensions = (width, height)
        arg_dict = {'input': source_path, 'dimensions': dimensions}

        with self.assertRaises(FileNotFoundError):
            expand_page.process_args(arg_dict)


class TestRunner(unittest.TestCase):

    def test_expand_page_runner(self):
        source_file = 'sample/sample.tiff'
        target_file = 'sample/sample2.tiff'
        width = 2160
        height = 3060
        dimensions = (width, height)
        arg_dict = {
            'input': source_file,
            'output': target_file,
            'dimensions': dimensions
        }
        
        action = expand_page.process_args(arg_dict)
        expand_page.Runner.setup(action)
        expand_page.Runner.execute(action)

        target_file_exists = os.path.exists(target_file)
        os.remove(target_file)

        self.assertTrue(target_file_exists)

