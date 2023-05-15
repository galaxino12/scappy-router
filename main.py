import requests
import sys
from bs4 import BeautifulSoup


def main():
    islink = str(sys.argv[1])
    if islink.startswith('https://'):
        withurl(islink)
    elif islink.endswith('.txt'):
        withfile(islink)
    else:
        print("Your first argument isn´t a url or a name file.")


def withfile(file):
    file_to_read = open(file, 'r')
    lines_to_read = file_to_read.readlines()

    for line in lines_to_read:
        spider(str(line))
    file_to_read.close()


def withurl(url):
    spider(url)


def spider(arg1):
    r = requests.get(arg1)
    src = str(sys.argv[2])
    raw = BeautifulSoup(r.content, 'html.parser')
    title = raw.find('h1', {'class': 'Headline-headline-2FXIq Headline-black-OogpV ArticleHeader-headline-NlAqj'})
    raw_content = raw.find_all('p', {'class': 'Paragraph-paragraph-2Bgue ArticleBody-para-TD_9x'})
    author = raw.find('a', {'class': 'TextLabel__text-label___3oCVw TextLabel__black-to-orange___23uc0 '
                                     'TextLabel__serif___3lOpX Byline-author-2BSir'})
    file = open(src, 'w+')
    file.write('\n')
    file.writelines('Title: ' + title.text)
    file.write('\n')
    file.writelines('By: ' + author.text)
    file.write('\n')
    for i in main_content(raw_content):
        file.write(i.get_text())
        file.write('\n')
    file.close()


def main_content(soup):
    cont = []
    for string in soup:
        cont.append(string)
    return cont


if __name__ == '__main__':
    main()
