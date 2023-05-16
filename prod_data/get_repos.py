import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    response = requests.get('https://github.com/vinta/awesome-python')
    doc = BeautifulSoup(response.text, 'html.parser')

    repo_link_els = doc.find_all('a')
    repo_links = []
    for repo_link_el in repo_link_els:
        if repo_link_el['href'].startswith('https://github.com/'):
            repo_links .append(repo_link_el['href'])
    
    with open("./python_repos.txt", "w") as text_file:
        text_file.write(','.join(repo_links))