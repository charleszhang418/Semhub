from semgrepper.repo_metadata import grab_metadata
from connector import Connector

if __name__ == '__main__':
    con = Connector.getConnectorInstance()
    cur = con.cursor()
    cur.execute('SELECT name, owner from Repository')
    repos = cur.fetchall()
    for name, owner in repos:
        metadata = grab_metadata(f'https://github.com/{owner}/{name}')
        cur.execute(f'UPDATE Repository SET stars = {metadata["stars"]} WHERE name = "{name}" AND owner = "{owner}"')
        con.commit()
        print('updated', name, owner)