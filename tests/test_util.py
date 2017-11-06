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


class TestFilesExist(unittest.TestCase):

    def test_files_exists_with_single_existing_file(self):
        existing_file = ['sample/sample.pdf']
        self.assertTrue(util.files_exist(existing_file))


    def test_files_exists_with_multiple_existing_files(self):
        existing_files = ['sample/sample.pdf', 'sample/sample.tiff']
        self.assertTrue(util.files_exist(existing_files))


    def test_files_exist_with_empty_input(self):
        empty_file_list = []
        self.assertTrue(util.files_exist(empty_file_list))


    def test_files_exist_with_nonexistent_file(self):
        nonexisting_files = ['foo.pdf', 'bar.pdf', 'baz.pdf']
        self.assertFalse(util.files_exist(nonexisting_files))


    def test_files_exist_with_nameless_file_with_extension(self):
        file_name = ['.pdf']
        try:
            util.files_exist(file_name)
        except:
            self.fail('files_exist threw an exception.')


    def test_files_exist_with_nameless_file_without_extension(self):
        file_name = ['']
        self.assertFalse(util.files_exist(file_name))


class TestTempDirectory(unittest.TestCase):

    def test_temp_directory(self):
        old_dir = '/foo/bar/baz/quux/'
        expected = '/foo/bar/baz/quux/__bookworm__/'
        result = util.temp_directory(old_dir)

        self.assertEqual(result, expected)

    def test_root_temp_directory(self):
        old_dir = '/'
        expected = '/__bookworm__/'
        result = util.temp_directory(old_dir)

        self.assertEqual(result, expected)


class TestWithExtension(unittest.TestCase):

    def test_with_extension(self):
        before = {'path': '/foo/bar/baz/', 'files': ['quux1.tiff', 'quux2.tiff', 'quux3.tiff', 'quux4.jpg']}
        after  = {'path': '/foo/bar/baz/', 'files': ['quux1.tiff', 'quux2.tiff', 'quux3.tiff']}

        res = util.with_extension('.tiff', before)
        self.assertEqual(res, after)


    def test_with_extension_should_correct_with_no_leading_period_in_input_extension(self):
        before = {'path': '/foo/bar/baz/', 'files': ['quux1.tiff', 'quux2.tiff', 'quux3.tiff', 'quux4.jpg']}
        after  = {'path': '/foo/bar/baz/', 'files': ['quux1.tiff', 'quux2.tiff', 'quux3.tiff']}
        
        # with_extension should be able to correct for no leading period.
        res = util.with_extension('tiff', before)
        self.assertEqual(res, after)


class TestQuotedString(unittest.TestCase):

    def run_with(self, string, expected):
        result = util.quoted_string(string)

        self.assertEqual(result, expected)


    def test_quoted_string_empty_string(self):
        self.run_with(string='', expected='\"\"')
    
    def test_quoted_string_closed_in_quotes(self):
        string='\"foo bar baz quux!\"'
        self.run_with(string=string, expected=f'{string}')
    
    def test_quoted_string_with_one_quote_head(self):
        string='\"foo bar baz quux'
        self.run_with(string=string, expected=f'{string}\"')

    def test_quoted_string_with_one_quote_tail(self):
        string='foo bar baz quux\"'
        self.run_with(string=string, expected=f'\"{string}')

    def test_quoted_string_no_quotes(self):
        string = 'foo bar baz quux!'
        self.run_with(string=string, expected=f'\"{string}\"')

