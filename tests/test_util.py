import unittest
import bookworm.util as util


class TestCommandFunction(unittest.TestCase):

    def test_temp_file_name(self):
        old_file = 'foo.pdf'
        new_file = 'foo.bookworm.pdf'

        self.assertEqual(util.temp_file_name(old_file), new_file)


    def test_temp_directory(self):
        old_dir = '/foo/bar/baz/quux/'
        new_dir = '/foo/bar/baz/quux/__bookworm__/'

        self.assertEqual(util.temp_directory(old_dir), new_dir)


    def test_with_extension(self):
        before = {'path': '/foo/bar/baz/', 'files': ['quux1.tiff', 'quux2.tiff', 'quux3.tiff', 'quux4.jpg']}
        after  = {'path': '/foo/bar/baz/', 'files': ['quux1.tiff', 'quux2.tiff', 'quux3.tiff']}

        res = util.with_extension('.tiff', before)

        self.assertEqual(res, after)

        # with_extension should be able to correct for no leading period.
        res = util.with_extension('tiff', before)

        self.assertEqual(res, after)

    def test_quoted_string(self):
        string = "\"foo bar baz quux!\""
        final_string = '{}'.format(string)

        self.assertEqual(util.quoted_string(string), final_string)

        # String with only one quote in it.
        string = '\"foo bar baz quux'
        final_string = '{}\"'.format(string)

        self.assertEqual(util.quoted_string(string), final_string)

        string = 'foo bar baz quux\"'
        final_string = '\"{}'.format(string)

        self.assertEqual(util.quoted_string(string), final_string)

