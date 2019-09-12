from dotenv import load_dotenv
import os
import requests
import datetime
import dateutil.parser
import json

load_dotenv()

# i.e. theAlexPatin
OWNER = os.getenv('GITHUB_USERNAME')

# a personal access token created at https://github.com/settings/tokens
GITHUB_KEY = os.getenv('GITHUB_KEY')

GITHUB_API = 'https://api.github.com'

START_DATE = datetime.datetime.now() - datetime.timedelta(days=365)

def get_commits_by_repo(repo):
    page = 1
    res = []
    while True:
        url = '{}/repos/{}/commits?since={}&page={}'.format(GITHUB_API, repo, START_DATE.isoformat(), page)
        data = _github_request(url)
        res.extend([datetime.datetime.strptime(c['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ") for c in data])
        if len(data) < 30:
            break
        page += 1
    return res

def get_user_repo_list():
    url = '{}/user/repos?sort=updated&type=all&per_page=100'.format(GITHUB_API, OWNER)
    res = _github_request(url)
    return [r['full_name'] for r in res if datetime.datetime.strptime(r['updated_at'], "%Y-%m-%dT%H:%M:%SZ") > START_DATE]

def _github_request(url):
    return requests.get(url, headers={ 'Authorization': 'token ' + GITHUB_KEY }).json()

def _get_date_format(date):
    year = str(date.year)
    month = str(date.month)
    if len(month) == 1:
        month = '0'+month
    day = str(date.day)
    if len(day) == 1:
        day = '0'+day
    return '{}-{}-{}'.format(year, month, day)

def main():
    dates = dict()
    repos = get_user_repo_list()
    for r in repos:
        commits = get_commits_by_repo(r)
        print(len(commits))
        for d in commits:
            date = _get_date_format(d)
            if date in dates:
                dates[date] += 1
            else:
                dates[date] = 1
    with open('commits.json', 'w') as f:
        json.dump(dates, f, indent=4)
if __name__ == '__main__':
    main()
