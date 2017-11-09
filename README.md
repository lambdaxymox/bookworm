# Bookworm

**Bookworm** is a python utility for automating batch document scan processing.
They are designed to normalize the dimensions of scanned pages to ensure they all have the same resolution and dimensions. The program's purpose is to fit inside a workflow of packing the pages of a book into a document such as a PDF or DJVU file, and running optical character recognition.

## Usage

[Fork](https://github.com/stallmanifold/bookworm) and run
```bash
$ python bookworm.py unpack-pdf -i /path/to/file.pdf  
```
to unpack a pdf. Run
```bash
$ python bookworm.py expand-page -d WIDTHxHEIGHT -i /path/to/file.tiff
```
to expand the dimensions to WIDTH and HEIGHT in pixels. Run the command
```bash
$ python bookworm.py change-resolution -r RESOLUTION -i /path/to/file.tiff
```
to change the resolution of a page, in pixels per inch, without modifying the page contents.


## Dependencies

These following programs are required to run bookworm.
```
GhostScript
ImageMagick
Python 3 ( >= 3.6)
```
