# Bookworm

**Bookworm** is a set of python scripts for automating parts of the workflow
for processing scanned PDF files.

These are some python scripts for automating PDF file manipulation workflow. They
are meant for normalizing the dimensions of scanned pages and ensuring they are all
the same resolution. These help automate the process of preparing the scanned pages of
a book for packing into a PDF or DJVU and running optical character recognition.

Usage
=====

Fork [fork]https://github.com/stallmanifold/bookworm and run

```
$ python bookworm.py unpack-pdf -i /path/to/file.pdf  
```  

to unpack a pdf. Run

```    
$ python bookworm.py expand-page -d WIDTHxHEIGHT -i /path/to/file.tiff
```

to expand the dimensions to WIDTH and HEIGHT in pixels. Run the command

```
$ python bookworm.py change-resolution -r RESOLUTION -i /path/to/file.tiff
```
to change the resolution of a page, in pixels per inch, without modifying the page contents.


Dependencies
============

These following programs are required to run bookworm.
```
GhostScript
ImageMagick
Python 3 ( >= 3.6)
```
