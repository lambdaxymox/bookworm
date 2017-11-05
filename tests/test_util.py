import unittest
import bookworm.util as util


class TestTempFileName(unittest.TestCase):

    def test_temp_file_name(self):
        old_file = 'foo.pdf'
        expected = 'foo.bookworm.pdf'
        result = util.temp_file_name(old_file)

        self.assertEqual(result, expected)

    def test_temp_file_name_should_correctly_apply_to_nameless_file(self):
        old_file = '.pdf'
        expected = '.bookworm.pdf'
        result = util.temp_file_name(old_file)

        self.assertEqual(result, expected)


class TestTempDirectory(unittest.TestCase):

    def test_temp_directory(self):
        old_dir = '/foo/bar/baz/quux/'
        expected = '/foo/bar/baz/quux/__bookworm__/'
        result = util.temp_directory(old_dir)

        self.assertEqual(result, expected)


class TestWithExtension(unittest.TestCase):

    def test_with_extension(self):
        before = {'path': '/foo/bar/baz/', 'files': ['quux1.tiff', 'quux2.tiff', 'quux3.tiff', 'quux4.jpg']}
        after  = {'path': '/foo/bar/baz/', 'files': ['quux1.tiff', 'quux2.tiff', 'quux3.tiff']}

        res = util.with_extension('.tiff', before)

        self.assertEqual(res, after)

        # with_extension should be able to correct for no leading period.
        res = util.with_extension('tiff', before)

        self.assertEqual(res, after)


class TestQuotedString(unittest.TestCase):

    def test_quoted_string_empty_string(self):
        string = ""
        expected = "\"\""
        result = util.quoted_string(string)

        self.assertEqual(result, expected)

    def test_quoted_string_closed_in_quotes(self):
        string = "\"foo bar baz quux!\""
        expected = '{}'.format(string)
        result = util.quoted_string(string)

        self.assertEqual(result, expected)

    def test_quoted_string_with_one_quote_head(self):
        string = '\"foo bar baz quux'
        expected = '{}\"'.format(string)
        result = util.quoted_string(string)

        self.assertEqual(result, expected)

    def test_quoted_string_with_one_quote_tail(self):
        string = 'foo bar baz quux\"'
        expected = '\"{}'.format(string)
        result = util.quoted_string(string)

        self.assertEqual(expected, result)

    def test_quoted_string_no_quotes(self):
        string = "foo bar baz quux!"
        expected = '\"{}\"'.format(string)
        result = util.quoted_string(string)

        self.assertEqual(expected, result)

