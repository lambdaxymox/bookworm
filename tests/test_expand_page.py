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


class TestProcessArgs(unittest.TestCase):

    def setUp(self):
        self.source_file = 'sample/sample.tiff'
        self.width = 2160
        self.height = 3060
        self.arg_dict = dict(
            input = self.source_file,
            dimensions = (self.width, self.height),
        )

    def use_source_file(self, source_file):
        self.source_file = source_file
        self.arg_dict['input'] = source_file

    def use_dimensions(self, width=None, height=None):
        if width:
            self.width = width
            self.arg_dict['dimensions'] = (width, self.height)
        if height:
            self.height = height
            self.arg_dict['dimensions'] = (self.width, height)


    def test_process_args(self):
        """
        The argument processor should produce a valid instance of
        a page action given valid inputs.
        """
        action = expand_page.process_args(self.arg_dict)

        # No exception occurred.
        self.assertIsInstance(action, expand_page.ExpandPageWithFill)
        self.assertEqual(action.width, self.width)
        self.assertEqual(action.height, self.height)
        self.assertEqual(action.source_file, self.source_file)


    def test_process_args_should_reject_bad_dimensions(self):
        """
        The new dimensions of the input page should both be integer values.
        You cannot define the notion of width and height by other means in
        terms of pixels.
        """
        self.use_dimensions(height="Potato")
        with self.assertRaises(TypeError):
            expand_page.process_args(self.arg_dict)


    ### TODO: a setup action should handle this!!!
    def test_process_args_should_reject_non_existent_file(self):
        """
        The argument processor should only generate a valid input if the
        input file actually exists.
        """
        self.use_source_file('sample/sample_doesnotexist.tiff')
        with self.assertRaises(FileNotFoundError):
            expand_page.process_args(self.arg_dict)


class TestMultipleExpandPages(unittest.TestCase):

    def setUp(self):
        self.width = 2160
        self.height = 3060
        self.arg_dict = dict(
            input = 'sample/test_tiffs/',
            dimensions = (self.width, self.height)
        )

    def use_source_path(self, source_path):
        self.arg_dict['input'] = source_path

    def get_source_files(self):
        source_path = self.arg_dict['input']
        source_files = os.listdir(source_path)
        full_source_files = []
        for source_file in source_files:
            full_source_files += os.path.join(source_path, source_file)

        return full_source_files


    def test_process_args_should_generate_multiple_actions_from_input_directory(self):
        """
        If an input directory exists and has multiple tiff files in it, the
        argument processor should find them and pack them together into a
        multiple page action.
        """
        multi_actions = expand_page.process_args(self.arg_dict)
        source_files = self.get_source_files()
        for action in multi_actions.values():
            self.assertIsInstance(action, expand_page.ExpandPageWithFill)
            self.assertEqual(action.width, self.width)
            self.assertEqual(action.height, self.height)
            self.assertTrue(action.source_file in source_files)


    def test_process_args_should_reject_non_existent_input_directory(self):
        """
        If the input directory does not exist, there is no work to be done.
        """
        self.use_source_path('sample/directory/does/not/exist/')
        with self.assertRaises(FileNotFoundError):
            expand_page.process_args(self.arg_dict)


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

