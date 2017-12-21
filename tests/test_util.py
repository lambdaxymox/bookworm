import os
import unittest
import bookworm.util as util
import hypothesis.strategies as st

from hypothesis import given, example


class TestTempFileName(unittest.TestCase):

    file_extensions = st.sampled_from(['.pdf', '.djvu'])
    file_names = st.tuples(st.text(), file_extensions)

    @st.composite
    def temp_file_name_data(draw, file_names=file_names):
        old_file = draw(file_names)
        old_file_name = old_file[0] + old_file[1]
        new_file_name = old_file[0] + '.bookworm' + old_file[1]
        
        return dict(
            old_file_name = old_file_name,
            new_file_name = new_file_name
        )

    @given(temp_file_name_data())
    @example(dict(old_file_name='.pdf', new_file_name='.bookworm.pdf'))
    def test_temp_file_name(self, file_dict):
        """
        Given a valid input file, ``temp_file_name`` should generate the temporary file
        name string, including in the case where the file name is empty.
        """
        result = util.temp_file_name(file_dict['old_file_name'])
        expected = file_dict['new_file_name']

        assert result == expected


class TestFilesExist(unittest.TestCase):

    existing_files = st.lists(elements=st.sampled_from([
        'sample/sample.pdf',
        'sample/sample.tiff',
        'sample/test_tiffs/sample_001.tiff',
        'sample/test_tiffs/sample_002.tiff',
        'sample/test_tiffs/sample_003.tiff',
        'sample/test_tiffs/sample_004.tiff',
        'sample/test_tiffs/sample_005.tiff'
    ]))

    nonexisting_files = st.lists(elements=st.text(), min_size=1)

    @given(existing_files)
    @example([])
    def test_files_exist_with_existing_files(self, existing_files):
        """
        Given a list of zero or more files all of which exist, ``files_exist`` should
        return ``True`` i.e., all the files exist.
        """
        assert util.files_exist(existing_files)


    @given(nonexisting_files)
    @example(['.pdf'])
    @example([''])
    def test_files_exist_with_nonexisting_files(self, nonexisting_files):
        """
        Given a nonempty collection of files that don't exist, ``files_exist`` should 
        return ``False``.
        """
        assert not util.files_exist(nonexisting_files)


class TestTempDirectory(unittest.TestCase):
   
    @st.composite
    def file_paths(draw):
        file_path = draw(st.lists(elements=st.text()))
        return '/'.join(file_path)

    @st.composite
    def temp_directory_data(draw, file_paths=file_paths()):
        old_file_path = draw(file_paths)
        new_file_path = os.path.join(old_file_path, '__bookworm__/')
        return dict(old_path = old_file_path, new_path = new_file_path)


    @given(temp_directory_data())
    @example(dict(
        old_path = '/foo/bar/baz/quux/', 
        new_path = '/foo/bar/baz/quux/__bookworm__/'
    ))
    @example(dict(old_path = '/', new_path = '/__bookworm__/'))
    @example(dict(old_path = '', new_path = '__bookworm__/'))
    def test_temp_directory(self, file_dict):
        """
        Given any file directory, ``temp_directory`` should return the correct
        path to the temporary directory. Also, that directory should exist
        inside the input directory.
        """
        result = util.temp_directory(file_dict['old_path'])
        expected = file_dict['new_path']

        assert result == expected


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


    @st.composite
    def test_case(draw, quote_or_not=st.sampled_from(['\"', ''])):
        raw_string = draw(st.characters(blacklist_characters=['\"', '\'']))
        string = f'{draw(quote_or_not)}{raw_string}{draw(quote_or_not)}'
        expected = f'\"{raw_string}\"'
        
        return dict(string = string, expected = expected)


    @given(test_case())
    @example(dict(string="", expected="\"\""))
    @example(dict(string="\"foo bar baz quux!\"", expected="\"foo bar baz quux!\""))
    @example(dict(string="\"foo bar baz quux!", expected="\"foo bar baz quux!\""))
    @example(dict(string="foo bar baz quux!\"", expected="\"foo bar baz quux!\""))
    @example(dict(string="foo bar baz quux!", expected="\"foo bar baz quux!\""))
    def test_quoted_string_unquoted_string(self, test_case):
        """
        Given an arbitrary string that is not necessarily exclosed in quotes, 
        ``quoted_string`` enclose the string in exactly one pair of quotes.
        """
        assert util.quoted_string(test_case['string']) == test_case['expected']


    @given(test_case())
    def test_quoted_string_is_singly_quoted(self, test_case):
        """
        Given a string that is already enclosed in quotes, ``quoted_string``
        should not change the string.
        """
        expected = util.quoted_string(test_case['string'])      
        assert util.quoted_string(expected) == expected

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

