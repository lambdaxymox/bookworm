import unittest
import bookworm.unpack_pdf as unpack_pdf
import bookworm.util       as util
import os, os.path


class TestUnpackPDF(unittest.TestCase):

    def setUp(self):
        self.source_file = 'sample/sample.pdf'
        self.target_path = f'sample/{util.default_subdirectory()}'
        self.arg_dict = dict(
            input = self.source_file,
            output = self.target_path
        )

    def test_unpack_pdf(self):
        """
        UnpackPDF should derive a local directory from the path to the source pdf file.
        """
        action = unpack_pdf.make(self.source_file)

        self.assertIsInstance(action, unpack_pdf.UnpackPDF)


    def test_unpack_pdf_generates_correct_terminal_command(self):
        """
        An ``UnpackPDF`` object should be a valid python subprocess.
        """
        action = unpack_pdf.process_args(self.arg_dict)
        terminal_command = [
            'gs', '-q', '-dNOPAUSE', '-dBATCH',   '-sDEVICE=tiff24nc', 
            '-sCompression=lzw',     '-r600x600', 
            f'-sOutputFile={self.target_path}_Page_%04d.tiff',
            self.source_file
        ]
        
        self.assertEqual(action.as_subprocess(), terminal_command)


class TestUnpackPDFProcessArgs(unittest.TestCase):

    def setUp(self):
        self.arg_dict = dict(
            input = 'sample/sample.pdf',
            output = f'sample/{util.default_subdirectory()}'
        )

    def test_process_args(self):
        """
        The ``UnpackPDF`` class's ``process_args`` method should correctly
        take an input pdf, and create an action that will pass the contents
        of the pdf into a default subdirectory in the same directory as the 
        pdf file.
        """
        action = unpack_pdf.process_args(self.arg_dict)

        self.assertIsInstance(action, unpack_pdf.UnpackPDF)


class TestRunner(unittest.TestCase):

    def setUp(self):
        self.arg_dict = dict(
            input = 'sample/sample.pdf',
            output = f'sample/{util.default_subdirectory()}'
        )

    def use_source_file(self, source_file):
        self.arg_dict['input'] = source_file

    def use_target_path(self, target_path):
        self.arg_dict['output'] = target_path

    def test_unpack_pdf_setup(self):
        """
        An UnpackPDF object's setup function should make the target directory
        if it does not exist.
        """
        action = unpack_pdf.process_args(self.arg_dict)
        try:
            unpack_pdf.Runner.setup(action)
            if not os.path.isdir(self.arg_dict['output']):
                raise FileExistsError
        except:
            self.fail()
        finally:
            unpack_pdf.Runner.cleanup(action)

        self.assertEqual(action.target_dir, self.arg_dict['output'])


    def test_action_setup_should_reject_non_existent_output_directory(self):
        """
        The UnpackPDF class's ``setup`` method should fail when the 
        output directory does not exist.
        """
        self.use_source_file('sample/doesnotexist.pdf')
        self.use_target_path('sample/')
        action = unpack_pdf.process_args(self.arg_dict)

        with self.assertRaises(FileNotFoundError):
            unpack_pdf.Runner.setup(action)


    def test_unpack_pdf_cleanup_should_remove_files_and_directory(self):
        """
        An UnpackPDF object's setup function should make the target directory
        if it does not exist.
        """
        action = unpack_pdf.process_args(self.arg_dict)
            
        unpack_pdf.Runner.setup(action)
        unpack_pdf.Runner.cleanup(action)

        self.assertFalse(os.path.exists(action.target_dir))


    def test_unpack_pdf_should_not_write_to_a_directory_with_existing_files(self):
        self.use_target_path('sample/test_tiffs')
        action = unpack_pdf.process_args(self.arg_dict)    
        try:
            unpack_pdf.Runner.setup(action)
            unpack_pdf.Runner.execute(action)
        except FileExistsError:
            self.assertTrue(os.path.exists(action.target_dir))


    def test_unpack_pdf_runner_executes_entire_process(self):
        action = unpack_pdf.process_args(self.arg_dict)
        try:
            unpack_pdf.Runner.setup(action)
            unpack_pdf.Runner.execute(action)
        except FileNotFoundError as e:
            unpack_pdf.Runner.cleanup(action)
            self.fail()
        else:
            unpack_pdf.Runner.cleanup(action)


    def test_unpack_pdf_runner_unpacks_a_pdf_to_a_directory(self):
        action = unpack_pdf.process_args(self.arg_dict)
        try:
            unpack_pdf.Runner.setup(action)
            unpack_pdf.Runner.execute(action)
        except FileNotFoundError as e:
            unpack_pdf.Runner.cleanup(action)
            self.fail()

        if not os.path.isdir(self.arg_dict['output']):
            unpack_pdf.Runner.cleanup(action)
            self.fail()

        unpack_pdf.Runner.cleanup(action)

