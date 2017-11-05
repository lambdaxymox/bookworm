import unittest
import bookworm.command as command


class TestCommandFunction(unittest.TestCase):

    def test_temp_file_name(self):

        old_file = 'foo.pdf'
        new_file = 'foo.bookworm.pdf'

        self.assertEqual(command.temp_file_name(old_file), new_file)


    def test_temp_directory(self):

        old_dir = '/foo/bar/baz/quux/'
        new_dir = '/foo/bar/baz/quux/__bookworm__/'

        self.assertEqual(command.temp_directory(old_dir), new_dir)


    def test_with_extension(self):

        before = {'path': '/foo/bar/baz/', 'files': ['quux1.tiff', 'quux2.tiff', 'quux3.tiff', 'quux4.jpg']}
        after  = {'path': '/foo/bar/baz/', 'files': ['quux1.tiff', 'quux2.tiff', 'quux3.tiff']}

        res = command.with_extension('.tiff', before)

        self.assertEqual(res, after)

        # with_extension should be able to correct for no leading period.
        res = command.with_extension('tiff', before)

        self.assertEqual(res, after)

    def test_quoted_string(self):

        string = "\"foo bar baz quux!\""
        final_string = '{}'.format(string)

        self.assertEqual(command.quoted_string(string), final_string)

        # String with only one quote in it.
        string = '\"foo bar baz quux'
        final_string = '{}\"'.format(string)

        self.assertEqual(command.quoted_string(string), final_string)

        string = 'foo bar baz quux\"'
        final_string = '\"{}'.format(string)

        self.assertEqual(command.quoted_string(string), final_string)

    
class TestResolution(unittest.TestCase):

    def test_make_resolution_should_only_accept_certain_units(self):

        resolution_val = 600
        resolution_units = 'Potato'

        self.assertRaises(ValueError, command.Resolution.make_resolution, resolution_val, resolution_units)


    def test_make_resolution_should_reject_negative_values(self):

        resolution_val = -600
        resolution_units = 'PixelsPerInch'

        self.assertRaises(ValueError, command.Resolution.make_resolution, resolution_val, resolution_units)

    def test_make_resolution_should_reject_non_integer_values(self):

        resolution_val = 600.1
        resolution_units = 'PixelsPerInch'

        self.assertRaises(TypeError, command.Resolution.make_resolution, resolution_val, resolution_units)

