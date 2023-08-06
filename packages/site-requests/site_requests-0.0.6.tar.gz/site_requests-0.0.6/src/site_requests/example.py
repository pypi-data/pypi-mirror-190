from bs4 import BeautifulSoup as bs4
import requests

print('実行ファイル')
def get_data(url, tag):
    
    gets = requests.get(url)
    soup = bs4(gets.text, 'html.parser')
    results = []
    for tag in soup.find_all(tag):
        results.append(tag.text)

    return results


if __name__ == '__main__':
    url = 'https://zerofromlight.com/blogs'
    tag = 'h5'

    for text in get_data(url, tag):
        print(text)
