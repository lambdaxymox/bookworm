import command
import os.path

class PackPDF(command.PDFCommand):
    def __init__(self):
        pass

def pack_pdf(source, target):
    raise NotImplemented

"""
Repacking a PDF is not presently implemented. This can always be done after editing and OCRing with
Adobe Acrobat or a similar program.
"""
def process_args(arg_dict):
    raise NotImplemented