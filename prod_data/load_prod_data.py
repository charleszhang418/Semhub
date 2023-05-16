import mysql.connector

if __name__ == '__main__':
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="semhub"
    )

    cur = con.cursor()
    with open('./python_repos.txt', 'r') as f:
        github_urls = f.read().split(',')
        for github_url in github_urls:
            try:
                cur.execute(f'INSERT INTO RepositoryQueue (github_url) VALUES ("{github_url}");')
                con.commit()
            except:
                pass
    con.commit()



