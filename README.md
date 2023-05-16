# SemHub
SemHub is a static code analysis data to see overall trends and summaries regarding code quality of repositories. The dataset will be scraped from GitHub repositories, getting general information on the repos as well as code analysis data through SemGrep. SemHub will regularly scrape well-known repos (most starred) it has not seen before and add it to the dataset. Users can also view data on specific repo links of their choice which will then also be added to the dataset.

## Installation
1. Create a venv
2. From root dir, run `pip install -r requirements.txt`
3. Go to frontend
4. Run `npm i`

## Running it
### Backend
From root, run `python3 -m flask --app backend run -p 3001`.

Also, run `python3 backend/scan_queue.py &` to in background process new repos.

Also, run mysql and create a database called semhub.

To load the database, go to either test_data or prod_data and load the dump from test_data.sql or dump.sql respectively. To actually load the data from scratch, you can use the UI to submit github urls and it will scrape them for you. Or, you can submit repo urls yourself to RepositoryQueue table. load_prod_data.py is an example of how to do this for the repos in `python_repos.txt`.

### Frontend
From frontend folder, run `npm start`

## Project structure
```
SemHub
📦SemHub
 ┣ 📂backend
 ┃ ┣ 📂semgrepper // analysis tool
 ┃ ┣ 📜__init__.py // flask server
 ┣ 📂frontend
 ┃ ┣ 📂public
 ┃ ┣ 📂src // frontend website
 ┣ 📂load_test_data
 ┃ ┣ 📜load_sample_data.py // script to load data from json files
 ┃ ┗ 📜test_data.sql // db dump
 ┣ 📂prod_data // production dump
 ┣ 📂migrations // database setup
```

## Load test data
Start up your mysql database, and run load_sample_data.py. itll parse and load the 3 json files!!  
Alternatively, there is a test_data.sql dump you can load from.

## Features
1. Summary - click summary to see overall summary of all repos, or search for a specific one
2. Rank all repos - view all repos by number of issues
3. Add new repo - click submit a repo to submit a github url to be analysed added to the database
4. Rank by impact - view all high impact repos - a score given to a repo by the severity of its issues. Repos with more severe issues will have a higher impact. Repos need at least 20 issues a one HIGH level issue to be in this list.
5. Update - when ranking all repos, you can click the update button to update its meta data.
6. Overall impact - view all repos and sort by ones that have the least amount of high impact issues. Good for seeing which repos have good code quality.

Also have a scraper that continously scans for repos to be added.