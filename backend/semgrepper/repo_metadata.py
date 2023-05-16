import requests
from bs4 import BeautifulSoup
import json
import time

cookies = {
    'logged_in': 'no',
    'preferred_color_mode': 'light',
    'tz': 'America%2FToronto',
}

headers = {
    'authority': 'github.com',
    'accept': 'application/json',
    'accept-language': 'en-CA,en;q=0.9',
    'cache-control': 'no-cache',
    # 'cookie': '_gh_sess=j0hnM1VODaxW5iy%2BR5i6fgHG7D%2FT96auihQeWjU2dk1l7lunvi7gxBz4XSZAEQbTPq4rB3WIBDIZpqEikq4WiQsh7WK1WFC0gPGTxjqCp%2Bz0skj%2FKx2PNqjNC5FGrKm9oVn5u3cBRErWTJnyaqJfKVBlIGlD6can77g5c%2Bwwq2PsqPe0eD4ikSRO%2BLVHKKDrs5k7rg0XcKZKgqhd499WKEP3HVi8rP37kQ87HNAbaDa4BncQRjz4Al8bNdmiJ02xppGn0frF1X2n0Dcye2IBCg%3D%3D--YnU1dteverOULGAK--7FtpMNtI8GenC5%2BMDUMcUQ%3D%3D; _octo=GH1.1.586058855.1679782559; logged_in=no; preferred_color_mode=light; tz=America%2FToronto',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

CONTRIBUTOR_ENDPOINT = '/graphs/contributors-data'


def _is_org(html: str):
    soup = BeautifulSoup(html, "html.parser")
    return len(soup.find_all('a', {'data-hovercard-type': 'organization'})) > 0


def _get_stars(html: str):
    soup = BeautifulSoup(html, "html.parser")
    star_count_title = soup.find(
        'span', {'id': 'repo-stars-counter-star'})['title']
    star_count_int = int(star_count_title.replace(',', ''))
    return star_count_int


def _get_contributors(url: str):
    response = requests.get(
        f'{url}{CONTRIBUTOR_ENDPOINT}', cookies=cookies, headers=headers)
    try:
        data = json.loads(response.text)
    except:
        return []
    return [payload['author']['login'] for payload in data]


def grab_metadata(url: str, retries=3):
    owner, repo_name = url.split('/')[-2:]
    for _ in range(retries):
        try:
            response = requests.get(url)
            contributors = _get_contributors(url)
            org = _is_org(response.text)
            if len(contributors) == 0 and not org:
                contributors = [owner]
            else:
                contributors = []
            break
        except:
            response = None
            time.sleep(1)

    if response is None:
        raise Exception('we probably got rate limited..')

    return {
        'owner': owner,
        'repo_name': repo_name,
        'contributors': contributors,
        'is_org': org,
        'stars': _get_stars(response.text)
    }


if __name__ == '__main__':
    # test
    url = "https://github.com/RustPython/RustPython"
    # url = 'https://github.com/patrickzbhe/DeepSnow'
    print(grab_metadata(url))
