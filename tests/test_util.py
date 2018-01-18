import os
import bookworm.sample_data as sample
import bookworm.util as util
import hypothesis.strategies as st

from hypothesis import given, example


class TestTempFileName:

    file_extensions = st.sampled_from(['.pdf', '.djvu'])
    file_names = st.tuples(
        st.characters(blacklist_characters=['\"']), file_extensions
    )

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
        Given a valid input file, ``temp_file_name`` should generate a temporary file
        name string, including in the case where the file name is empty.
        """
        result = util.temp_file_name(file_dict['old_file_name'])
        expected = file_dict['new_file_name']

        assert result == expected


class TestFilesExist:

    existing_files = st.lists(
        elements=st.sampled_from(sample.SAMPLE_FILES)
    )

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


class TestTempDirectory:
   
    @st.composite
    def file_paths(draw):
        file_path = draw(st.lists(elements=st.text()))
        return '/'.join(file_path)

    @st.composite
    def temp_directory_data(draw, file_paths=file_paths()):
        old_file_path = draw(file_paths)
        new_file_path = os.path.join(
            old_file_path, util.default_subdirectory()
        )
        return dict(old_path = old_file_path, new_path = new_file_path)


    @given(temp_directory_data())
    @example(dict(
        old_path = '/foo/bar/baz/quux/', 
        new_path = f'/foo/bar/baz/quux/{util.default_subdirectory()}'
    ))
    @example(dict(old_path = '/', new_path = f'/{util.default_subdirectory()}'))
    @example(dict(old_path = '', new_path = util.default_subdirectory()))
    def test_temp_directory(self, file_dict):
        """
        Given any file directory, ``temp_directory`` should return the correct
        path to the temporary directory. Also, that directory should exist
        inside the input directory.
        """
        result = util.temp_directory(file_dict['old_path'])
        expected = file_dict['new_path']

        assert result == expected


class TestWithExtension:

    def test_with_extension(self):
        """
        Given a set of files with different file extensions, the 
        ``with_extension`` function should correctly identify which
        files inside that directory have the input file extension.
        """
        before = dict(
            path = '/foo/bar/baz/',
            files =  ['quux1.tiff', 'quux2.tiff', 'quux3.tiff', 'quux4.jpg']
        )
        expected = dict(
            path = '/foo/bar/baz/',
            files = ['quux1.tiff', 'quux2.tiff', 'quux3.tiff']
        )

        result = util.with_extension('.tiff', before)
        assert result == expected


    def test_with_extension_should_correct_with_no_leading_period_in_input_extension(self):
        """
        ``with_extension`` should accept a file extension string with or
        with no leading period.
        """
        before = dict(
            path =  '/foo/bar/baz/',
            files =  ['quux1.tiff', 'quux2.tiff', 'quux3.tiff', 'quux4.jpg']
        )
        expected = dict(
            path = '/foo/bar/baz/',
            files = ['quux1.tiff', 'quux2.tiff', 'quux3.tiff']
        )
        
        result = util.with_extension('tiff', before)
        assert result == expected

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

        assert with_period == without_period


class TestQuotedString:

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
        Given an arbitrary string that is not necessarily enclosed in quotes, 
        ``quoted_string`` encloses the string with exactly one pair of quotes.
        """
        assert util.quoted_string(test_case['string']) == test_case['expected']


    @given(test_case())
    def test_quoted_string_is_idempotent(self, test_case):
        """
        Given a string that is already enclosed in quotes, ``quoted_string``
        should not change the string.
        """
        expected = util.quoted_string(test_case['string'])      
        assert util.quoted_string(expected) == expected

