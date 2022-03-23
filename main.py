# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import pandas as pd
import textract as textract


def parse_paragraphs_from_pdf(file):
    text = textract.process(file, method='pdfminer')
    # print(text)
    # pattern = re.compile(b"\\s+\\n\\n\\s+")
    output_text = text.decode('utf-8')
    # print(output_text)
    pattern = re.compile("\\s{3,}")
    paragraphs = re.split(pattern, output_text)
    for (index, para) in enumerate(paragraphs):
        paragraphs[index] = para.replace("\n", " ")
    return paragraphs

if __name__ == '__main__':
    paragraphs = parse_paragraphs_from_pdf('resources/200309-sustainable-finance-teg-final-report-taxonomy-annexes_en.pdf')
    print( paragraphs )
