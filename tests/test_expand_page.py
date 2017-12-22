import pytest
import os
import bookworm.expand_page as expand_page

from collections import namedtuple


class TestExpandPageWithFill:

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

        assert isinstance(action, expand_page.ExpandPageWithFill)


class TestProcessArgs:

    @pytest.fixture
    def arg_dict(self):
        return dict(
            input = 'sample/sample.tiff',
            width = 2160,
            height = 3060,
            dimensions = (2160, 3060),
        )

    def use_source_file(self, arg_dict, source_file):
        arg_dict['input'] = source_file

    def use_dimensions(self, arg_dict, width=None, height=None):
        if width:
            arg_dict['width'] = width
            arg_dict['dimensions'] = (width, arg_dict['height'])
        if height:
            arg_dict['height'] = height
            arg_dict['dimensions'] = (arg_dict['width'], height)


    def test_process_args(self, arg_dict):
        """
        The argument processor should produce a valid instance of
        a page action given valid inputs.
        """
        action = expand_page.process_args(arg_dict)

        # No exception occurred.
        assert isinstance(action, expand_page.ExpandPageWithFill)
        assert action.width == arg_dict['dimensions'][0]
        assert action.height == arg_dict['dimensions'][1]
        assert action.source_file == arg_dict['input']


    def test_process_args_should_reject_bad_dimensions(self, arg_dict):
        """
        The new dimensions of the input page should both be integer values.
        You cannot define the notion of width and height by other means in
        terms of pixels.
        """
        self.use_dimensions(arg_dict, height="Potato")
        with pytest.raises(TypeError):
            expand_page.process_args(arg_dict)


    def test_process_args_should_reject_non_existent_file(self, arg_dict):
        """
        The argument processor should only generate a valid input if the
        input file actually exists.
        """
        self.use_source_file(arg_dict, 'sample/sample_doesnotexist.tiff')
        with pytest.raises(FileNotFoundError):
            expand_page.process_args(arg_dict)


class TestMultipleExpandPages:

    @pytest.fixture
    def arg_dict(self):
        return dict(
            input = 'sample/test_tiffs/',
            dimensions = (2160, 3060)
        )

    def use_source_path(self, arg_dict, source_path):
        arg_dict['input'] = source_path

    def get_source_files(self, arg_dict):
        source_path = arg_dict['input']
        source_files = os.listdir(source_path)
        full_source_files = []
        for source_file in source_files:
            full_source_files.append(os.path.join(source_path, source_file))

        return full_source_files


    def test_process_args_should_generate_multiple_actions_from_input_directory(self, arg_dict):
        """
        If an input directory exists and has multiple tiff files in it, the
        argument processor should find them and pack them together into a
        multiple page action.
        """
        multi_actions = expand_page.process_args(arg_dict)
        source_files = self.get_source_files(arg_dict)
        for action in multi_actions.values():
            assert isinstance(action, expand_page.ExpandPageWithFill)
            assert action.width == arg_dict['dimensions'][0]
            assert action.height == arg_dict['dimensions'][1]
            assert action.source_file in source_files


    def test_process_args_should_reject_non_existent_input_directory(self, arg_dict):
        """
        If the input directory does not exist, there is no work to be done.
        """
        self.use_source_path(arg_dict, 'sample/directory/does/not/exist/')
        with pytest.raises(FileNotFoundError):
            expand_page.process_args(arg_dict)


class TestRunner:

    Data = namedtuple('Data', 'target_file arg_dict')

    @pytest.fixture
    def fixture(self):
        data = self.Data(
            target_file = 'sample/sample2.tiff',
            arg_dict = dict(
                input = 'sample/sample.tiff',
                output = 'sample/sample2.tiff',
                dimensions = (2160, 3060),
            )
        )

        yield data
        os.remove(data.target_file)


    def test_expand_page_runner(self, fixture):        
        action = expand_page.process_args(fixture.arg_dict)
        expand_page.Runner.setup(action)
        expand_page.Runner.execute(action)

        assert os.path.exists(fixture.target_file)

