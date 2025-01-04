import pyttsx3, PyPDF2

path_to_book = input("Enter the path to the pdf \n")
pdfreader = PyPDF2.PdfFileReader(open(r'path_to_book', 'rb'))
speaker = pyttsx3.init()

for page_num in (pdfreader.numPages):
    text = pdfreader.getPage(page_num).extract_text
    clean_text = text.strip().replace('\n', ' ')
    print(clean_text)

name_of_file = input("Enter name of output fine you want \n")
speaker.save_to_file(clean_text, f'{name_of_file}.mp3')
speaker.runAndWait()

speaker.stop()