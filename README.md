# Bookworm

**Bookworm** is a python utility for automating batch document scan processing.
It is designed to normalize the dimensions of scanned pages to ensure they all have the same resolution and dimensions. Its purpose is to fit inside a workflow for packing the pages of a book into a document such as a `pdf` or `djvu` file, and running optical character recognition. Bookworm works cross-platform on Mac, Linux, Windows, or BSD.

## Installation
To install `bookworm`, [Fork](https://github.com/stallmanifold/bookworm) and run the following commands in the terminal or command line.
```bash
$ python setup.py sdist
$ python setup.py install --user
```
Alternatively, you can install it directly using pip.
```bash
pip install git+https://github.com/stallmanifold/bookworm.git
```

## Usage
There are two ways to run bookworm: (1) run from source; (2) install it. In order to run from source, see the section **Usage From Source**. This section describes how to use it on your local machine. Enter
```bash
$ bookworm unpack-pdf -i "/path/to/file.pdf"
```
to unpack a pdf. Run
```bash
$ bookworm expand-page -d WIDTHxHEIGHT -i "/path/to/file.tiff"
```
to expand the dimensions to WIDTH and HEIGHT in pixels. Run the command
```bash
$ bookworm change-resolution -r RESOLUTION -i "/path/to/file.tiff"
```
Run the command
```bash
$ bookworm resample-page -r RESOLUTION -i "/path/to/file.tiff"
```
to resample a page at a new RESOLUTION. Finally, for further information on how to use bookworm, enter
```bash
$ bookworm --help
```

## Usage From Source
There are two ways to run bookworm.
[Fork](https://github.com/stallmanifold/bookworm) and run
```bash
$ python src/bookworm.py unpack-pdf -i "/path/to/file.pdf"
```
to unpack a pdf. Run
```bash
$ python src/bookworm.py expand-page -d WIDTHxHEIGHT -i "/path/to/file.tiff"
```
to expand the dimensions to WIDTH and HEIGHT in pixels. Run the command
```bash
$ python src/bookworm.py change-resolution -r RESOLUTION -i "/path/to/file.tiff"
```
to change the resolution of a page, in pixels per inch, without modifying the page contents.Run the command
```bash
$ python src/bookworm.py resample-page -r RESOLUTION -i "/path/to/file.tiff"
```
to resample a page at a new RESOLUTION. Finally, for further information on how to use bookworm, enter
```bash
$ python src/bookworm.py --help
```

## Dependencies
Bookworm requires the following programs to be installed on your system.
```
GhostScript
ImageMagick
Python 3 (>= 3.6)
```

## Uninstallation
Should you decide you no longer want to use `bookworm` on your system, you can remove it via `pip` in terminal or command line.
```bash
$ pip uninstall bookworm
```
