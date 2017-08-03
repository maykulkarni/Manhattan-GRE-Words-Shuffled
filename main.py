from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from random import shuffle


class Word:
    """Used to store a word, and its information"""

    def __init__(self, name, information):
        self.name = name
        self.name = [x for x in self.name.split('\n') if x is not '']
        self.name[0] = ' ' * (50 - len(self.name[0]) / 2) + self.name[0]
        self.name[1] = ' ' * (50 - len(self.name[1]) / 2) + self.name[1]
        self.name[2] = ' ' * (50 - len(self.name[2]) / 2) + self.name[2]
        if len(self.name) == 4:
            self.name[3] = ' ' * (50 - len(self.name[3]) / 2) + self.name[3]
        self.name = '\n'.join(self.name)
        self.information = information.replace('Usage:', '\nUsage:')
        self.information = self.information.replace('Related Words:', '\nRelated Words:')
        self.information = self.information.replace('More Info:', '\nMore Info:')

    def __str__(self):
        return self.name + '\n\n' + self.information


def get_pdf_content(file_name):
    # stolen from : https://stackoverflow.com/a/21564675
    fp = file(file_name, 'rb')
    resource_manager = PDFResourceManager()
    return_string = StringIO()
    codec = 'utf-8'
    la_params = LAParams()
    device = TextConverter(resource_manager, return_string, codec=codec, laparams=la_params)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(resource_manager, device)
    # Process each page contained in the document.
    ctr = 0
    for page in PDFPage.get_pages(fp):
        ctr += 1
        if ctr < 4:
            continue
        interpreter.process_page(page)
        file_name = return_string.getvalue()

    return file_name.split('\x0c')


def process(output_file_name, input_file_name):
    words = []
    file_content = get_pdf_content(input_file_name)[:-1]
    for i in range(0, len(file_content), 2):
        words.append(Word(file_content[i], file_content[i + 1]))

    shuffle(words)

    with open(output_file_name, 'w') as f:
        for word in words:
            f.write('*' * 100)
            f.write('\n')
            f.write(str(word))
            f.write('\n')


if __name__ == '__main__':
    process('manhattan_essential.txt', 'Manhattan500Essential.pdf')
    process('manhattan_advanced.txt', 'Manhattan500Advanced.pdf')