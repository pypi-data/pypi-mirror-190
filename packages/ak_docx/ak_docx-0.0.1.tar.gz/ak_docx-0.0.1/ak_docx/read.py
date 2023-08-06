import docx2txt
from pathlib import Path

def read_docx(filepath:Path) -> str:
    return docx2txt.process(str(filepath))