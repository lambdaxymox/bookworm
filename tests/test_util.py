import unittest
import bookworm.util as util


class TestTempFileName(unittest.TestCase):

    def test_temp_file_name(self):
        """
        We should generate the correct file name under normal conditions.
        """
        old_file = 'foo.pdf'
        expected = 'foo.bookworm.pdf'
        result = util.temp_file_name(old_file)

        self.assertEqual(result, expected)


    def test_temp_file_name_should_correctly_apply_to_nameless_file(self):
        """
        ``temp_file_name`` should correctly handle files with no name but
        a file extension.
        """
        old_file = '.pdf'
        expected = '.bookworm.pdf'
        result = util.temp_file_name(old_file)

        self.assertEqual(result, expected)


class TestFilesExist(unittest.TestCase):

    def test_files_exists_with_single_existing_file(self):
        """
        Given a single file that we know exists, ``files_exist`` should 
        return ``True``.
        """
        existing_file = ['sample/sample.pdf']
        self.assertTrue(util.files_exist(existing_file))


    def test_files_exists_with_multiple_existing_files(self):
        """
        Given a collection of files that we know exist, ``files_exists``
        should return ``True``.
        """
        existing_files = ['sample/sample.pdf', 'sample/sample.tiff']
        self.assertTrue(util.files_exist(existing_files))


    def test_files_exist_with_empty_input(self):
        """
        Given an empty collection of files, ``files_exist`` should 
        trivially return ``True``.
        """
        empty_file_list = []
        self.assertTrue(util.files_exist(empty_file_list))


    def test_files_exist_with_nonexistent_file(self):
        """
        Given a collection of files that don't exist, ``files_exist`` should
        return ``False``.
        """
        nonexisting_files = ['foo.pdf', 'bar.pdf', 'baz.pdf']
        self.assertFalse(util.files_exist(nonexisting_files))


    def test_files_exist_with_nameless_file_with_extension(self):
        """
        Given a file with no name, but just a file extension, ``files_exist``
        should return ``False``
        """
        file_name = ['.pdf']
        self.assertFalse(util.files_exist(file_name))


    def test_files_exist_with_nameless_file_without_extension(self):
        """
        Given a file of zero length, ``files_exist`` should return ``False``.
        """
        file_name = ['']
        self.assertFalse(util.files_exist(file_name))


class TestTempDirectory(unittest.TestCase):

    def test_temp_directory(self):
        """
        Given any file directory, ``temp_directory`` should return the correct
        path to the temporary directory. Also, that directory should exist
        inside the input directory.
        """
        old_dir = '/foo/bar/baz/quux/'
        expected = '/foo/bar/baz/quux/__bookworm__/'
        result = util.temp_directory(old_dir)

        self.assertEqual(result, expected)

    def test_root_temp_directory(self):
        """
        Given the root directory, ``temp_directory`` should correctly place
        the temporary folder inside root.
        """
        old_dir = '/'
        expected = '/__bookworm__/'
        result = util.temp_directory(old_dir)

        self.assertEqual(result, expected)


class TestWithExtension(unittest.TestCase):

    def test_with_extension(self):
        """
        Given a set of files with different file extensions, the 
        ``with_extension`` functio should correctly identify which
        files inside that directory have the input file extension.
        """
        before = dict(
            path = '/foo/bar/baz/',
            files =  ['quux1.tiff', 'quux2.tiff', 'quux3.tiff', 'quux4.jpg']
        )
        after = dict(
            path = '/foo/bar/baz/',
            files = ['quux1.tiff', 'quux2.tiff', 'quux3.tiff']
        )

        res = util.with_extension('.tiff', before)
        self.assertEqual(res, after)


    def test_with_extension_should_correct_with_no_leading_period_in_input_extension(self):
        """
        ``with_extension`` should accept a file extension string with or
        without a leading period.
        """
        before = dict(
            path =  '/foo/bar/baz/',
            files =  ['quux1.tiff', 'quux2.tiff', 'quux3.tiff', 'quux4.jpg']
        )
        after = dict(
            path = '/foo/bar/baz/',
            files = ['quux1.tiff', 'quux2.tiff', 'quux3.tiff']
        )
        
        # with_extension should be able to correct for no leading period.
        res = util.with_extension('tiff', before)
        self.assertEqual(res, after)

    def test_with_extension_invariant_under_leading_period(self):
        """
        Given a set of files, ``with_extension`` should correctly identify the
        same files that match a given file extension with or without the
        leading period in the extension name.
        """
        files_dict = dict(
            path = '/foo/bar/baz/', 
            files = ['quux1.tiff', 'quux2.tiff', 'quux3.tiff', 'quux4.jpg']
        )

        with_period = util.with_extension('.tiff', files_dict)
        without_period = util.with_extension('tiff', files_dict)

        self.assertEqual(with_period, without_period)


class TestQuotedString(unittest.TestCase):

    def run_with(self, string, expected):
        result = util.quoted_string(string)

        self.assertEqual(result, expected)


    def test_quoted_string_empty_string(self):
        """
        ``quoted_string`` should be able to quote an empty string.
        """
        self.run_with(string='', expected='\"\"')
    
    def test_quoted_string_closed_in_quotes(self):
        """
        Given a string that is already exclosed in quotes, ``quoted_string``
        should not change the string.
        """
        string='\"foo bar baz quux!\"'
        self.run_with(string=string, expected=f'{string}')
    
    def test_quoted_string_with_one_quote_head(self):
        """
        Given a string with a quote symbol at the start of the string,
        ``quoted_string`` should only quote the tail of the string.
        """
        string='\"foo bar baz quux'
        self.run_with(string=string, expected=f'{string}\"')

    def test_quoted_string_with_one_quote_tail(self):
        """
        Given a string with a quote symbol at the end of the string,
        ``quoted_string`` should only quote at the head of the string.
        """
        string='foo bar baz quux\"'
        self.run_with(string=string, expected=f'\"{string}')

    def test_quoted_string_no_quotes(self):
        """
        Given a string with no quoted, ``quoted_string`` should close the
        string in quotes.
        """
        string = 'foo bar baz quux!'
        self.run_with(string=string, expected=f'\"{string}\"')

