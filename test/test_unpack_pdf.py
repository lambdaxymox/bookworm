import unittest
import unpack_pdf
import command
import os, os.path

class TestUnpackPDF(unittest.TestCase):

    def test_unpack_pdf(self):
        """
        UnpackPDF should derive a local directory from the path to the source pdf file.
        """
        source_pdf = './foo/bar/baz/quux.pdf'
        target_dir = './foo/bar/baz/' + command.default_subdirectory()

        terminal_command = unpack_pdf.unpack_pdf(source_pdf)

        self.assertEqual(terminal_command.image_dir(), target_dir)


    def test_process_args(self):

        source_pdf = 'sample/sample.pdf'
        target_dir = 'sample/__bookworm__/'
        arg_dict = {'input': source_pdf, 'output': target_dir}

        if not os.path.isdir(target_dir):
            os.mkdir(target_dir)
        
        action = unpack_pdf.process_args(arg_dict)
        os.rmdir(target_dir)

        self.assertIsInstance(action, unpack_pdf.UnpackPDF)


    def test_action_setup_should_reject_non_existent_output_directory(self):

        source_pdf = 'sample/doesnotexist.pdf'
        target_dir = 'sample/'
        arg_dict = {'input': source_pdf, 'output': target_dir}

        action = unpack_pdf.process_args(arg_dict)

        self.assertRaises(FileNotFoundError, action.setup)


    def test_unpack_pdf_generates_correct_terminal_command(self):
        source_pdf = 'sample/sample.pdf'
        target_dir = 'sample/__bookworm__/'
        arg_dict = {'input': source_pdf, 'output': target_dir}

        if not os.path.isdir(target_dir):
            os.mkdir(target_dir)

        action = unpack_pdf.process_args(arg_dict)

        terminal_command = [
                'gs', '-q', '-dNOPAUSE', '-dBATCH',   '-sDEVICE=tiff24nc', 
                '-sCompression=lzw',     '-r600x600', '-sOutputFile='+target_dir+'_Page_%4d.tiff', 
                source_pdf
            ]

        os.rmdir(target_dir)
        
        self.assertEqual(action.as_python_subprocess(), terminal_command)


    def test_unpack_pdf_setup(self):
        """
        An UnpackPDF object's setup function should make the target directory if it does not exist.
        """
        source_pdf = 'sample/sample.pdf'
        target_dir = 'sample/' + command.default_subdirectory()
        arg_dict = {'input': source_pdf, 'output': target_dir}

        action = unpack_pdf.process_args(arg_dict)

        try:
            action.setup()
        except FileNotFoundError as e:
            os.rmdir(target_dir)
            self.fail()

        if not os.path.isdir(target_dir):
            os.rmdir(target_dir)
            self.fail()

        os.rmdir(target_dir)

        self.assertEqual(action.target_dir, target_dir)
