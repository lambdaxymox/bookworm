import pytest
import os
import bookworm.sample_data as sample


class TestSampleData:

    def test_sample_root(self):
        """
        The sample root retured from the sample module should exist.
        """
        assert os.path.exists(sample.SAMPLE_ROOT)


    def test_sample_data(self):
        """
        The sample files should actually exist in the sample directory.
        """
        for file in sample.SAMPLE_FILES:
            assert os.path.exists(file)


    def test_get_sample_files(self):
        """
        The sample files returned by the ``get_sample_files`` function should
        actually exist.
        """
        for file in sample.get_sample_files(sample.SAMPLE_ROOT):
            assert os.path.exists(file)

