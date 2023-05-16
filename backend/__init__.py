import os
import mysql.connector
from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
from backend.semgrepper.repo_metadata import grab_metadata
from backend.connector import Connector
import re

def sanitize_url(url: str):
    if not url.startswith('https://github.com/'):
        raise Exception('bad url')

    owner_and_name = url[len('https://github.com/'):].split('/')

    if len(owner_and_name) != 2:
        raise Exception('bad url')

    for part in owner_and_name:
        if re.match(r'^[a-zA-Z0-9-_]{1,100}$', part):
            return part
        else:
            raise Exception(f"Input string '{part}' is not a valid GitHub username or repository name.")

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    @app.route('/summary')
    def summary():
        con = Connector.getConnectorInstance()
        cur = con.cursor()

        query_params = request.args.to_dict()

        repo_name = query_params.get('repo_name', '')
        if repo_name:
            repos = cur.execute(f'SELECT names.name, count(name) FROM (SELECT name FROM Repository WHERE name LIKE "{repo_name}%") names LEFT JOIN Issue on names.name = Issue.repo_name GROUP BY names.name')
            all_repos = cur.fetchall()
            return jsonify(all_repos)
        else:
      
            totalReposQuery = 'SELECT count(*) FROM Repository'
            totalOrgsQuery = 'SELECT count(*) FROM Organization'
            totalOwnersQuery = 'SELECT count(*) FROM Owner'
            totalIssuesQuery = 'SELECT count(*) FROM Issue'

            cur.execute(totalReposQuery)
            totalRepos = cur.fetchall()[0][0]
            cur.execute(totalOrgsQuery)
            totalOrgs = cur.fetchall()[0][0]
            cur.execute(totalOwnersQuery)
            totalOwners = cur.fetchall()[0][0]
            cur.execute(totalIssuesQuery)
            totalIssues = cur.fetchall()[0][0]

            

            return jsonify({
                'totalRepos': totalRepos,
                'totalOrgs': totalOrgs,
                'totalUsers': totalOwners - totalOrgs,
                'totalOwners': totalOwners,
                'totalIssues': totalIssues,
            })
        
    @app.route('/rank_all')
    def rank_all():
        query_params = request.args.to_dict()
        con = Connector.getConnectorInstance()
        cur = con.cursor()
        page = query_params.get('page', 0)
        print(query_params)
        cur.execute(f'SELECT repo_name, owner, count(*) as issues, rank() over (ORDER BY count(*) asc) as ranking FROM Issue GROUP BY repo_name, owner LIMIT 20 OFFSET {int(page) * 20}')
        return jsonify({
            'rankings': cur.fetchall(),
        })
    
    @app.route('/add_to_queue', methods=['POST'])
    def add_to_queue():

        github_url = request.json['github_url']

        con = Connector.getConnectorInstance()
        cur = con.cursor()
        sanitize_url(github_url)
        cur.execute(f'INSERT INTO RepositoryQueue (github_url) VALUES ("{github_url}");')
        con.commit()
        return f"You submitted: {github_url}"

    @app.route('/compare_repos')
    def compare_repos():
        con = Connector.getConnectorInstance()
        cur = con.cursor()
        file_name = 'backend/SQLFiles/quantifyImpact.sql'
        with open(file_name, 'r') as sql_file:
            commands = cur.execute(sql_file.read(), multi=True)
            for command in commands:
                print(command)
        file_name = 'backend/SQLFiles/compareRepos.sql'
        with open(file_name, 'r') as sql_file:
            cur.execute(sql_file.read(), multi=True)

        return jsonify({
            'impact': cur.fetchall()
        })
    
    @app.route('/top_repos')
    def top_repos():
        con = Connector.getConnectorInstance()
        cur = con.cursor()
        cur.execute('WITH repo_impact as (SELECT * FROM (SELECT R2.name, R2.owner, SUM(I.impact) as ovr_impact FROM Repository as R2 JOIN (SELECT repo_name, owner, QuantifyImpact(impact) as impact FROM Issue) as I ON R2.name = I.repo_name and R2.owner = I.owner GROUP BY R2.name, R2.owner) as R) SELECT * FROM repo_impact WHERE ovr_impact > (SELECT AVG(ovr_impact) FROM repo_impact)')
        return jsonify({
            'top_repos': cur.fetchall(),
        })
    
    @app.route('/update', methods=['POST'])
    def update():
        print(request.json)
        owner = request.json['owner']
        repo_name = request.json['repo_name']
        con = Connector.getConnectorInstance()
        cur = con.cursor()
        metadata = grab_metadata(f'https://github.com/{owner}/{repo_name}')
        cur.execute(f'UPDATE Repository SET stars = {metadata["stars"]} WHERE name = "{repo_name}" AND owner = "{owner}"')
        con.commit()
        print(owner, repo_name)
        return f'nice'


    return app



