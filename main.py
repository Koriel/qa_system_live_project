# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import pandas as pd

import textract as textract


def parse_text_from_pdf(file):
    text = textract.process(file, method='pdfminer')
    # print(text)
    # pattern = re.compile(b"\\s+\\n\\n\\s+")
    output_text = text.decode('utf-8')
    save_pre_parsed_text(output_text)
    return output_text

def parse_paragraphs_from_text(text):
    def split_paragraphs(unsplit_text):
        pattern = re.compile("\\s{3,}")
        return re.split(pattern, unsplit_text)
    # print(output_text)
    minimum_paragraph_length = 200
    paragraphs = split_paragraphs(text)
    cleaned_paragraphs = map(clean_text, paragraphs)
    large_paragraphs = filter(
        lambda x: len(x) >= minimum_paragraph_length,
        cleaned_paragraphs)
    return list(large_paragraphs)


def clean_text(text):
    text = text.replace("\n", " ")
    # text = re.sub(re.compile(""), " ", text)
    # text = re.sub("[^a-zA-Z0-9_\s!.?,;'\"()\[]{}]")

    # https://stackoverflow.com/questions/16205646/matching-invisible-characters-in-javascript-regex
    text = re.sub("[\xA0\x00-\x09\x0B\x0C\x0E-\x1F\x7F]", "", text)

    text = re.sub("\\s{2,}", " ", text)

    # https://stackoverflow.com/questions/150033/regular-expression-to-match-non-ascii-characters
    text = re.sub("[^\u0000-\u007F]", "", text)
    text = re.sub("[^\x00-\x7F]", "", text)

    text = text.strip()
    return text


def save_pre_parsed_text(text_to_save):
    file1 = open("pre-parsed-text.txt", 'w')
    # Reading from file
    file1.write(text_to_save)
    file1.close()


def load_pre_parsed_text():
    file1 = open("pre-parsed-text.txt")
    # Reading from file
    loaded_text = file1.read()
    file1.close()
    return loaded_text


if __name__ == '__main__':
    text = parse_text_from_pdf('resources/200309-sustainable-finance-teg-final-report-taxonomy-annexes_en.pdf')
    # text = load_pre_parsed_text()
    paragraphs = parse_paragraphs_from_text(text)
    df = pd.DataFrame({'paragraph': paragraphs})
    df.to_csv("eu_paragraphs.csv")
    print(paragraphs)

if __name__ == '__main__':
    text = parse_text_from_pdf('resources/W9126G22R0049_Solicitation.pdf')
    # text = load_pre_parsed_text()
    paragraphs = parse_paragraphs_from_text(text)
    df = pd.DataFrame({'paragraph': paragraphs})
    df.to_csv("eW9126G22R0049_Solicitation_paragraphs.csv")
    print(paragraphs)