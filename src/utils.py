import re
from docx import Document
from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph


ext_regex = re.compile('(\.[a-zA-Z0-9]+?$)')
number_regex = re.compile('^[\d\.]+')
table_number_regex = re.compile('^(?:Таблица |Табл. |.{0})([\d\.]*)')
unit_regex = re.compile('\(([^()]*)\)$')


def clean_text(text):
    text = text.replace('\n', ' ')
    text = ' '.join([word for word in text.split()])
    return text


def find_number_in_table_name(text):
    match = table_number_regex.search(text)
    if match:
        return match.group(1)


def find_unit_in_table_name(text):
    match = unit_regex.search(text)
    if match:
        return match.group(1)


def check_starts_with_number(text):
    match = number_regex.search(text)
    if match:
        return True
    else:
        return False


def iterate_paragraphs_and_tables(docx_document):
    if isinstance(docx_document, _Document):
        docx_document_elm = docx_document.element.body
    else:
        raise ValueError('ошибка при итерации по блокам docx')
    for child in docx_document_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, docx_document)
        elif isinstance(child, CT_Tbl):
            yield Table(child, docx_document)
