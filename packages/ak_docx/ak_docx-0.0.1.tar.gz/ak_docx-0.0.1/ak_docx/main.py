#!/usr/bin/env python
# coding: utf-8

import docx2txt, re
from ak_file import File
from ak_docx import read, write

class Word(File):
    def __init__(self, filepath:str =""):
        self.filepath=filepath
        File.__init__(self, filepath)
    
    @property
    def text(self) -> str:
        "Returns all the text in the document"
        return read.read_docx(self.filepath)

    def search_in_text(self, regex_str:str) -> re.Match:
        regex = re.compile(regex_str)
        return regex.search(self.text.replace('\n', ''))

    def __repr__(self):
        return f"Word(filepath=\"{self.filepath}\")"
