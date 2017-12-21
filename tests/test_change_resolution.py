import pytest
import bookworm.change_resolution as change_resolution
import os

from collections import namedtuple
from bookworm.resolution import Resolution


class TestChangeResolution:

    Data = namedtuple('Data', 'source_file resolution_val unit_str resolution')

    @pytest.fixture
    def fixture(self):
        return self.Data(
            source_file = 'sample/sample.tiff',
            resolution_val = 300,
            unit_str = 'PixelsPerInch',
            resolution = Resolution.make(300, 'PixelsPerInch') 
        )

    def test_change_resolution(self, fixture):
        """
        We should be able to create a page action that has the correct type.
        """
        action = change_resolution.make(fixture.resolution, fixture.source_file)
        assert isinstance(action, change_resolution.ChangeResolution)


class TestChangeResolutionProcessArgs:
    
    @pytest.fixture
    def arg_dict(self):
        return dict(
            input = 'sample/sample.tiff',
            output = 'sample/',
            units = 'PixelsPerInch'
        )

    def use_resolution_val(self, arg_dict, resolution_val):
        arg_dict['resolution'] = resolution_val


    def test_process_args(self, arg_dict):
        """
        The argument processor should correctly create a ``ChangeResolution``
        action under conditions where there is a positive resolution value when
        units are given.
        """
        self.use_resolution_val(arg_dict, 600)
        action = change_resolution.process_args(arg_dict)
        
        assert isinstance(action, change_resolution.ChangeResolution)
        assert action.source_file != action.target_file


    def test_process_args_should_reject_noninteger_values(self, arg_dict):
        """
        The argument processor should not accept a nonpositive, noninteger
        input value for the image resolution.
        """
        self.use_resolution_val(arg_dict, "Potato")
        with pytest.raises(TypeError):
            change_resolution.process_args(arg_dict)


    def test_process_args_should_reject_nonpositive_resolution_values(self, arg_dict):
        """
        The argument processor should not accept a negative input value for
        the image resolution.
        """
        self.use_resolution_val(arg_dict, -600)
        with pytest.raises(ValueError):
            change_resolution.process_args(arg_dict)


    def test_process_args_should_reject_resolution_value_of_zero(self, arg_dict):
        """
        The argument processor should not accept zero as an input value for
        the image resolution.
        """
        self.use_resolution_val(arg_dict, 0)
        with pytest.raises(ValueError):
            change_resolution.process_args(arg_dict)


class TestProcessArgsWithMissingResolutionUnits:

    @pytest.fixture
    def arg_dict(self):
        return dict(
            input = 'sample/sample.tiff',
            output = 'sample/',
            resolution = 300
        )

    def test_process_args_should_reject_missing_units(self, arg_dict):
        """
        The argument processor should not create a ``ChangeResolution`` action
        if the input resolution desired has no units.
        """
        with pytest.raises(KeyError):
            change_resolution.process_args(arg_dict)


class TestChangeResolutionRunner:

    @pytest.fixture
    def arg_dict(self):
        return dict(
            output = 'sample/',
            resolution = 300,
            units = 'PixelsPerInch'
        )

    def use_source_file(self, arg_dict, source_file):
        arg_dict['input'] = source_file


    def test_change_resolution_runner_process(self, arg_dict):
        self.use_source_file(arg_dict, 'sample/sample.tiff')
        action = change_resolution.process_args(arg_dict)

        try:
            change_resolution.Runner.setup(action)
            change_resolution.Runner.execute(action)
        except FileNotFoundError as e:
            pytest.fail()
        finally:
            change_resolution.Runner.cleanup(action)


    def test_runner_should_fail_if_source_does_not_exist(self, arg_dict):
        self.use_source_file(arg_dict, 'sample/doesnotexist.tiff')
        with pytest.raises(FileNotFoundError):
            action = change_resolution.process_args(arg_dict)
            change_resolution.Runner.setup(action)



class TestMultiChangePageResolution:

    @pytest.fixture
    def arg_dict(self):
        return dict(
            input = 'sample/test_tiffs/',
            resolution = 300,
            units = 'PixelsPerInch'
        )

    def get_source_files(self, arg_dict):
        source_path = arg_dict['input']
        source_files = os.listdir(source_path)
        full_source_files = []
        for source_file in source_files:
            full_source_files.append(os.path.join(source_path, source_file))

        return full_source_files


    def test_multi_page_change_resolution_should_generate_multiple_actions_from_input_directory(self, arg_dict):
        """
        Given a valid input directory with zero or more files in it, a multiple
        page change resolution action argument processor should correctly
        every valid input image and group them together into one action.
        """
        resolution = Resolution.make(
            arg_dict['resolution'], arg_dict['units']
        )
        multi_actions = change_resolution.process_args(arg_dict)
        
        for action in multi_actions.values():
            assert isinstance(action, change_resolution.ChangeResolution)


class TestMultiChangeResolutionProcessArgs:

    @pytest.fixture
    def arg_dict(self):
        return dict(
            input = 'sample/sample_tiffs/',
            units = 'PixelsPerInch',
        )

    def use_resolution_val(self, arg_dict, resolution_val):
        arg_dict['resolution'] = resolution_val

    def use_source_path(self, arg_dict, source_path):
        arg_dict['input'] = source_path


    def test_process_args_should_reject_non_existent_input_directory(self, arg_dict):
        """
        The arument processor should not accept an input directory that does
        not exist. Surely it is impossible to read a nonexistent input.
        """
        self.use_source_path(arg_dict, 'sample/directory_doesnotexist/')
        self.use_resolution_val(arg_dict, 600)

        with pytest.raises(FileNotFoundError):
            change_resolution.process_args(arg_dict)


    def test_process_args_should_reject_nonpositive_integer_resolutions(self, arg_dict):
        """
        The argument processor should reject negative and zero values for
        the new resolution for the image. It does not make sense to have 
        negative pixels per inch.
        """
        self.use_resolution_val(arg_dict, -600)
        with pytest.raises(ValueError):
            change_resolution.process_args(arg_dict)


    def test_process_args_should_reject_fractional_resolution_values(self, arg_dict):
        """
        The ``ChangeResolution`` action's argument processor should not accept
        fractional resolution values.
        """
        self.use_resolution_val(arg_dict, 600.1)
        with pytest.raises(TypeError):
            change_resolution.process_args(arg_dict)


class TestRunner:

    @pytest.fixture
    def fixture(self, request):
        arg_dict = dict(
            input = 'sample/sample.tiff',
            output = 'sample/sample2.tiff',
            resolution = 300,
            units = 'PixelsPerInch'
        )

        def fin():
            os.remove(arg_dict['output'])
        
        request.addfinalizer(fin)

        return arg_dict


    def test_change_resolution_runner(self, fixture):
        action = change_resolution.process_args(fixture)
        target_file = fixture['output']

        change_resolution.Runner.setup(action)
        change_resolution.Runner.execute(action)

        assert os.path.exists(target_file)

