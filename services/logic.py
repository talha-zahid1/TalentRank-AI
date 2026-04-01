import pdfplumber
import io
from docx import Document
import re
def pdf_opener(file):
    file_object=io.BytesIO(file)
    text=''
    with pdfplumber.open(file_object) as pdf:
        for page in pdf.pages:
            text+=page.extract_text() or "\n"
    return text
def python_docx(file):
    file_object=io.BytesIO(file)
    text='' 
    for paragraph in Document(file_object).paragraphs:
        text+=paragraph.text +"\n"
    return text
def cleaning_text(text):
    pattern1=r"\s{2,}"
    pattern2=r"[^a-zA-Z\d\s]"
    pattern3=r"\n{2,}"
    clean_text1=re.sub(pattern=pattern3,repl="\n",string=text)
    clean_text2=re.sub(pattern=pattern2,repl="",string=clean_text1)
    final_text=re.sub(pattern=pattern1,repl=" ",string=clean_text2)
    return final_text.strip()
