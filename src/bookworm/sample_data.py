import os


def get_sample_files(root):
    files = []
    for file_or_path in os.listdir(root):
        full_path = os.path.join(root, file_or_path)
        if os.path.isfile(full_path):
            files.append(full_path)           
        elif os.path.isdir(full_path):
            files += get_sample_files(full_path)
        else:
            raise FileNotFoundError(full_path)

    return files


SAMPLE_ROOT = 'sample'
TEST_TIFFS = os.path.join(SAMPLE_ROOT, 'test_tiffs')
SAMPLE_TIFF = os.path.join(SAMPLE_ROOT, 'sample.tiff')
SAMPLE_PDF = os.path.join(SAMPLE_ROOT, 'sample.pdf')
SAMPLE_FILES = get_sample_files(SAMPLE_ROOT)

