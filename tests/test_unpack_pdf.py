import pytest
import bookworm.unpack_pdf as unpack_pdf
import bookworm.util       as util
import os, os.path


class TestUnpackPDF:

    @pytest.fixture
    def arg_dict(self):
        return dict(
            input = 'sample/sample.pdf',
            output = f'sample/{util.default_subdirectory()}'
        )

    def test_unpack_pdf(self, arg_dict):
        """
        UnpackPDF should derive a local directory from the path to the source pdf file.
        """
        action = unpack_pdf.make(arg_dict['input'])
        assert isinstance(action, unpack_pdf.UnpackPDF)


    def test_unpack_pdf_generates_correct_terminal_command(self, arg_dict):
        """
        An ``UnpackPDF`` object should be a valid python subprocess.
        """
        action = unpack_pdf.process_args(arg_dict)
        target_path = arg_dict['output']
        terminal_command = [
            'gs', '-q', '-dNOPAUSE', '-dBATCH',   '-sDEVICE=tiff24nc', 
            '-sCompression=lzw',     '-r300x300', 
            f'-sOutputFile={target_path}_Page_%04d.tiff',
            arg_dict['input']
        ]
        
        assert action.as_subprocess() == terminal_command


class TestUnpackPDFProcessArgs:

    @pytest.fixture
    def arg_dict(self):
        return dict(
            input = 'sample/sample.pdf',
            output = f'sample/{util.default_subdirectory()}'
        )

    def test_process_args(self, arg_dict):
        """
        The ``UnpackPDF`` class's ``process_args`` method should correctly
        take an input pdf, and create an action that will pass the contents
        of the pdf into a default subdirectory in the same directory as the 
        pdf file.
        """
        action = unpack_pdf.process_args(arg_dict)
        assert isinstance(action, unpack_pdf.UnpackPDF)


class TestRunner:

    @pytest.fixture
    def arg_dict(self):
        return dict(
            input = 'sample/sample.pdf',
            output = f'sample/{util.default_subdirectory()}'
        )

    def use_source_file(self, arg_dict, source_file):
        arg_dict['input'] = source_file

    def use_target_path(self, arg_dict, target_path):
        arg_dict['output'] = target_path

    def test_unpack_pdf_setup(self, arg_dict):
        """
        An UnpackPDF object's setup function should make the target directory
        if it does not exist.
        """
        action = unpack_pdf.process_args(arg_dict)
        try:
            unpack_pdf.Runner.setup(action)
            if not os.path.isdir(arg_dict['output']):
                pytest.fail()
        except:
            pytest.fail()
        finally:
            unpack_pdf.Runner.cleanup(action)

        assert action.target_dir == arg_dict['output']


    def test_action_setup_should_reject_non_existent_output_directory(self, arg_dict):
        """
        The UnpackPDF class's ``setup`` method should fail when the 
        output directory does not exist.
        """
        self.use_source_file(arg_dict, 'sample/doesnotexist.pdf')
        self.use_target_path(arg_dict, 'sample/')
        action = unpack_pdf.process_args(arg_dict)
        with pytest.raises(FileNotFoundError):
            unpack_pdf.Runner.setup(action)


    def test_unpack_pdf_cleanup_should_remove_files_and_directory(self, arg_dict):
        """
        An UnpackPDF object's setup function should make the target directory
        if it does not exist.
        """
        action = unpack_pdf.process_args(arg_dict)
        try:
            unpack_pdf.Runner.setup(action)
        finally:
            unpack_pdf.Runner.cleanup(action)

        assert not os.path.exists(action.target_dir)


    def test_unpack_pdf_should_not_write_to_a_directory_with_existing_files(self, arg_dict):
        self.use_target_path(arg_dict, 'sample/test_tiffs')
        action = unpack_pdf.process_args(arg_dict)    
        try:
            unpack_pdf.Runner.setup(action)
            unpack_pdf.Runner.execute(action)
        except FileExistsError:
            assert os.path.exists(action.target_dir)


    def test_unpack_pdf_runner_executes_entire_process(self, arg_dict):
        action = unpack_pdf.process_args(arg_dict)
        try:
            unpack_pdf.Runner.setup(action)
            unpack_pdf.Runner.execute(action)
        except FileNotFoundError as e:
            pytest.fail()
        finally:
            unpack_pdf.Runner.cleanup(action)


    def test_unpack_pdf_runner_unpacks_a_pdf_to_a_directory(self, arg_dict):
        action = unpack_pdf.process_args(arg_dict)
        try:
            unpack_pdf.Runner.setup(action)
            unpack_pdf.Runner.execute(action)
            if not os.path.isdir(arg_dict['output']):
                pytest.fail()
        except:
            pytest.fail()
        finally:
            unpack_pdf.Runner.cleanup(action)

