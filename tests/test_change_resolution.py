import unittest
import bookworm.change_resolution as change_resolution
import os

from bookworm.resolution import Resolution


class TestChangeResolution(unittest.TestCase):

    def setUp(self):
        self.source_file = 'sample/sample.tiff'
        self.resolution_val = 300
        self.unit_str = 'PixelsPerInch'
        self.resolution = Resolution.make(self.resolution_val, self.unit_str) 

    def test_change_resolution(self):
        """
        We should be able to create a page action that has the correct type.
        """
        action = change_resolution.make(self.resolution, self.source_file)
        self.assertIsInstance(action, change_resolution.ChangeResolution)
        #self.assertNotEqual(action.target_file, action.source_file)


class TestChangeResolutionProcessArgs(unittest.TestCase):
    
    def setUp(self):
        self.arg_dict = dict(
            input = 'sample/sample.tiff',
            output = 'sample/',
            units = 'PixelsPerInch'
        )

    def use_resolution_val(self, resolution_val):
        self.arg_dict['resolution'] = resolution_val

    def test_process_args(self):
        """
        The argument processor should correctly create a ``ChangeResolution``
        action under conditions where there is a positive resolution value when
        units are given.
        """
        self.use_resolution_val(600)
        action = change_resolution.process_args(self.arg_dict)
        
        self.assertIsInstance(action, change_resolution.ChangeResolution)
        self.assertNotEqual(action.source_file, action.target_file)


    def test_process_args_should_reject_noninteger_values(self):
        """
        The argument processor should not accept a noninteger input value for
        the image resolution.
        """
        self.use_resolution_val("Potato")
        with self.assertRaises(TypeError):
            change_resolution.process_args(self.arg_dict)


    def test_process_args_should_reject_nonpositive_resolution_values(self):
        """
        The argument processor should not accept a negative input value for
        the image resolution.
        """
        self.use_resolution_val(-600)
        with self.assertRaises(ValueError):
            change_resolution.process_args(self.arg_dict)


    def test_process_args_should_reject_resolution_value_of_zero(self):
        """
        The argument processor should not accept zero as an input value for
        the image resolution.
        """
        self.use_resolution_val(0)
        with self.assertRaises(ValueError):
            change_resolution.process_args(self.arg_dict)


class TestProcessArgsWithMissingResolutionUnits(unittest.TestCase):

    def setUp(self):
        self.arg_dict = dict(
            input = 'sample/sample.tiff',
            output = 'sample/',
            resolution = 300
        )

    def test_process_args_should_reject_missing_units(self):
        """
        The argument processor should not create a ``ChangeResolution`` action
        if the input resolution desired has no units.
        """
        with self.assertRaises(KeyError):
            change_resolution.process_args(self.arg_dict)


class TestChangeResolutionRunner(unittest.TestCase):

    def setUp(self):
        self.arg_dict = dict(
            output = 'sample/',
            resolution = 300,
            units = 'PixelsPerInch'
        )

    def use_source_file(self, source_file):
        self.arg_dict['input'] = source_file


    def test_change_resolution_runner_process(self):
        self.use_source_file('sample/sample.tiff')
        action = change_resolution.process_args(self.arg_dict)

        try:
            change_resolution.Runner.setup(action)
            change_resolution.Runner.execute(action)
        except FileNotFoundError as e:
            self.fail()
        finally:
            change_resolution.Runner.cleanup(action)


    def test_runner_should_fail_if_source_does_not_exist(self):
        self.use_source_file('sample/doesnotexist.tiff')
        with self.assertRaises(FileNotFoundError):
            action = change_resolution.process_args(self.arg_dict)
            change_resolution.Runner.setup(action)


class TestMultiChangePageResolution(unittest.TestCase):

    def setUp(self):
        self.arg_dict = dict(
            input = 'sample/test_tiffs/',
            resolution = 300,
            units = 'PixelsPerInch'
        )

    def get_source_files(self):
        source_path = self.arg_dict['input']
        source_files = os.listdir(source_path)
        full_source_files = []
        for source_file in source_files:
            full_source_files.append(os.path.join(source_path, source_file))

        return full_source_files


    def test_multi_page_change_resolution_should_generate_multiple_actions_from_input_directory(self):
        """
        Given a valid input directory with zero or more files in it, a multiple
        page change resolution action argument processor should correctly
        every valid input image and group them together into one action.
        """
        resolution = Resolution.make(
            self.arg_dict['resolution'], self.arg_dict['units']
        )
        multi_actions = change_resolution.process_args(self.arg_dict)
        
        for action in multi_actions.values():
            self.assertIsInstance(action, change_resolution.ChangeResolution)


class TestMultiChangeResolutionProcessArgs(unittest.TestCase):

    def setUp(self):
        self.arg_dict = dict(
            input = 'sample/sample_tiffs/',
            units = 'PixelsPerInch',
        )

    def use_resolution_val(self, resolution_val):
        self.arg_dict['resolution'] = resolution_val

    def use_source_path(self, source_path):
        self.arg_dict['input'] = source_path


    def test_process_args_should_reject_non_existent_input_directory(self):
        """
        The arument processor should not accept an input directory that does
        not exist. Surely it is impossible to read a nonexistent input.
        """
        self.use_source_path('sample/directory_doesnotexist/')
        self.use_resolution_val(600)

        with self.assertRaises(FileNotFoundError):
            change_resolution.process_args(self.arg_dict)


    def test_process_args_should_reject_nonpositive_integer_resolutions(self):
        """
        The argument processor should reject negative and zero values for
        the new resolution for the image. It does not make sense to have 
        negative pixels per inch.
        """
        self.use_resolution_val(-600)
        with self.assertRaises(ValueError):
            change_resolution.process_args(self.arg_dict)


    def test_process_args_should_reject_fractional_resolution_values(self):
        """
        The ``ChangeResolution`` action's argument processor should not accept
        fractional resolution values.
        """
        self.use_resolution_val(600.1)
        with self.assertRaises(TypeError):
            change_resolution.process_args(self.arg_dict)


class TestRunner(unittest.TestCase):

    def setUp(self):
        self.arg_dict = dict(
            input = 'sample/sample.tiff',
            output = 'sample/sample2.tiff',
            resolution = 300,
            units = 'PixelsPerInch'
        )

    def tearDown(self):
        os.remove(self.arg_dict['output'])


    def test_change_resolution_runner(self):
        action = change_resolution.process_args(self.arg_dict)
        target_file = self.arg_dict['output']

        change_resolution.Runner.setup(action)
        change_resolution.Runner.execute(action)

        self.assertTrue(os.path.exists(target_file))

