import mysql.connector
import json
files = ['semgrep_json/coconut.json', 'semgrep_json/deepsnow.json', 'semgrep_json/flask.json']

if __name__ == '__main__':
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="semhub"
    )

    cur = con.cursor()
    cur.execute('DELETE FROM Issue')
    cur.execute('DELETE FROM File')
    cur.execute('DELETE FROM Repository')
    cur.execute('DELETE FROM User')
    cur.execute('DELETE FROM Owner')


    for file in files:
        data = {}
        with open(file, 'r') as f:
            data = json.load(f)
        if not data:
            continue
        cur.execute(f'INSERT INTO Owner (name) VALUES ("{data["owner"]}")')
        cur.execute(f'INSERT INTO User (name) VALUES ("{data["owner"]}")')
        cur.execute(f'INSERT INTO Repository (name, owner) VALUES ("{data["repo_name"]}", "{data["owner"]}")')
        # cur.execute(f'INSERT INTO Repository (name, owner) VALUES ("{data["repo_name"]}", "{data["owner"]}")')
        
        for file_path in data['paths']['scanned']:
            if not file_path.endswith('.py'):
                continue
            path_segments = file_path.split('/')[3:]
            name = path_segments[-1]
            path = '/'.join(path_segments)
            cur.execute(f'INSERT INTO File (name, language, path, repo_name, owner) VALUES ("{name}", "python", "{path}", "{data["repo_name"]}", "{data["owner"]}")')
 
        for result in data['results']:
            check_id = result['check_id']
            start_line = result['start']['line']
            end_line = result['end']['line']
            category = result['extra']['metadata']['category']
            impact = result['extra']['metadata']['impact']
            path_segments = result['path'].split('/')[3:]
  
         
            path = '/'.join(path_segments)
            if not path.endswith('.py'):
                continue
            #print(path, data["repo_name"], data["owner"])
            cur.execute(f'INSERT INTO Issue (check_id, start_line, end_line, category, impact, repo_name, owner, path) VALUES ("{check_id}", {start_line}, {end_line}, "{category}", "{impact}", "{data["repo_name"]}", "{data["owner"]}", "{path}")')
    con.commit()



