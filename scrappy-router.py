import requests, sys, os, re
from bs4 import BeautifulSoup
from pathlib import Path


def main():
    isurl = str(sys.argv[1])
    if isurl.startswith('https://'):
        spider(isurl)
    elif isurl.endswith('.txt'):
        withfile(isurl)
    else:
        print("Your first argument isn´t a url or a name file.")


def withfile(file):
    file_to_read = open(file, 'r')
    lines_to_read = file_to_read.readlines()

    for line in lines_to_read:
        spider(line)
    file_to_read.close()


def spider(url):
    response = requests.get(url)
    if response.status_code == 200:
        raw = BeautifulSoup(response.content, 'html.parser')
        title = raw.find('h1')
        author = raw.find(lambda t: t.name == "p" and ('Reporting' in t.text or 'Editing' in t.text ))
        main_content = raw.find_all('p', { 'data-testid':re.compile(r'paragraph-.')})
        content_paragraphs = []
        content_paragraphs.append(f'Title: {title.text} \n\n')
        content_paragraphs.append(f'Author/s: {author.text} \n\n')
        for paragraphs in main_content:
            content_paragraphs.append(paragraphs.get_text())
        content_paragraphs
        savingInfo((f"{title.text}"), content_paragraphs )
    else:
        print('Error getting page:', response.status_code)


def savingInfo(title, large_text):
    reg = r'[:/\<>|*"]'
    output = str(re.sub(reg, '-', title) + '.txt')
    file = open(output, 'w')
    for i in large_text:
        file.write(str(i+'\n'))
    file.close()
    if(Path(os.getcwd() + '\\' + output).is_file()):
        print("Item saved successfully!")   
    else:
        print("There was a problem saving")


if __name__ == '__main__':
    main()
