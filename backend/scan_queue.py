from connector import Connector
from semgrepper.semgrepper import semgrep_download
from semgrepper.repo_metadata import grab_metadata
from typing import Dict, Any
import time
from multiprocessing import Pool

LANGUAGES = {
    '.py': 'python',
    '.cpp': 'c++',
    '.js': 'javascript',
    '.ts': 'typescript'
}

def fetch_repos():
    con = Connector.getConnectorInstance()
    cur = con.cursor()
    cur.execute('SELECT * FROM RepositoryQueue')
    return [x[0] for x in cur.fetchall()]

def insert_repo_data(data: Dict[Any, Any], repo_url):
    con = Connector.getConnectorInstance()
    cur = con.cursor()
    cur.execute(f'SELECT * FROM Repository WHERE name = "{data["repo_name"]}" and owner = "{data["owner"]}"')
    if len(cur.fetchall()) > 0:
            # for now, don't rescan
            return

    cur.execute(f'SELECT * FROM Owner WHERE name = "{data["owner"]}"')
    if len(cur.fetchall()) == 0:
        # only insert owner if they don't exist
        cur.execute(f'INSERT INTO Owner (name) VALUES ("{data["owner"]}")')
        if data['is_org']:
            cur.execute(f'INSERT INTO Organization (name) VALUES ("{data["owner"]}")')
        else:
            cur.execute(f'INSERT INTO User (name) VALUES ("{data["owner"]}")')
    cur.execute(f'INSERT INTO Repository (name, stars, owner) VALUES ("{data["repo_name"]}", "{data["stars"]}", "{data["owner"]}")')
    
    for contributor in data['contributors']:
        cur.execute(f'SELECT * FROM Owner WHERE name = "{contributor}"')
        if len(cur.fetchall()) == 0:
                cur.execute(f'INSERT INTO Owner (name) VALUES ("{contributor}")')

        cur.execute(f'SELECT * FROM User WHERE name = "{contributor}"')
        if len(cur.fetchall()) == 0:
                cur.execute(f'INSERT INTO User (name) VALUES ("{contributor}")')
        cur.execute(f'INSERT INTO Contributor (user_name, repo_name, owner) VALUES ("{contributor}", "{data["repo_name"]}", "{data["owner"]}")')
        
    
    for file_path in data['paths']['scanned']:
        path_segments = file_path.split('/')[3:]
        name = path_segments[-1]
        path = '/'.join(path_segments)
        # small subset to make life easier

        # print(path_segments[-1].split('.')[-1])
        if path_segments[-1].split('.')[-1] in LANGUAGES:
            language = LANGUAGES[path_segments[-1]]
            print(language)
        else:
            continue
        cur.execute(f'INSERT INTO File (name, language, path, repo_name, owner) VALUES ("{name}", "{language}", "{path}", "{data["repo_name"]}", "{data["owner"]}")')
   
    for result in data['results']:
        check_id = result['check_id']
        start_line = result['start']['line']
        end_line = result['end']['line']
        category = result['extra']['metadata']['category']
        impact = result['extra']['metadata'].get('impact', 'MEDIUM')
        path_segments = result['path'].split('/')[3:]

        
        path = '/'.join(path_segments)
        if path_segments[-1].split('.')[-1] not in LANGUAGES:
            continue
        #print(path, data["repo_name"], data["owner"])
        cur.execute(f'INSERT INTO Issue (check_id, start_line, end_line, category, impact, repo_name, owner, path) VALUES ("{check_id}", {start_line}, {end_line}, "{category}", "{impact}", "{data["repo_name"]}", "{data["owner"]}", "{path}")')
    cur.execute(f'DELETE FROM RepositoryQueue WHERE github_url = "{repo_url}"')
    con.commit()

def scan_one(repo_url: str) -> None:
    try:
        print('SCANNING:', repo_url)
        metadata = grab_metadata(repo_url)
        scan_data = semgrep_download(repo_url)

        for key in metadata:
            scan_data[key] = metadata[key]

        insert_repo_data(scan_data, repo_url)
        print('SUCCESS!')
    except Exception as e:
        print('FAILED:', repo_url)
        print(e)

def scan_queue():
    repo_urls = fetch_repos()

    for repo_url in repo_urls:
        try:
            print('SCANNING:', repo_url)
            metadata = grab_metadata(repo_url)
            scan_data = semgrep_download(repo_url)

            for key in metadata:
                scan_data[key] = metadata[key]

            insert_repo_data(scan_data, repo_url)
            print('SUCCESS!')
        except Exception as e:
             print('FAILED:', repo_url)
             print(e)
            


         

if __name__ == '__main__':
    # while True:
    #     scan_queue()
    #     time.sleep(60)
    repo_urls = fetch_repos()
    for repo in repo_urls:
         scan_one(repo)
    # with Pool(1) as p:
    #      p.map(scan_one, repo_urls)
