import json
import datetime
import matplotlib.pyplot as plt
import numpy as np

with open('temperatures.json') as f:
    temp_data = json.load(f)

with open('commits.json') as f:
    commit_data = json.load(f)

START_DATE = datetime.datetime.now() - datetime.timedelta(days=365)

def _get_date_format(date):
    year = str(date.year)
    month = str(date.month)
    if len(month) == 1:
        month = '0'+month
    day = str(date.day)
    if len(day) == 1:
        day = '0'+day
    return '{}-{}-{}'.format(year, month, day)

def reject_outliers(data, m=2):
    res = list()
    for d in data:
        if abs(d - np.mean(data)) < m * np.std(data):
            res.append(d)
        else:
            res.append(np.mean(data))
    return res

def main():
    d = START_DATE
    temps = list()
    commits = list()
    X = 366
    BUCKETS=30
    for i in range(0, X):
        date = _get_date_format(d)
        if date in temp_data:
            temps.append(temp_data[date])
        if date in commit_data:
            commits.append(commit_data[date])
        else:
            commits.append(0)
        d = d + datetime.timedelta(days=1)
    temps = np.asarray(temps)
    temps = temps / np.linalg.norm(temps)
    commits = np.asarray(commits)
    commits = commits / np.linalg.norm(commits)
    for i in range(0, floor(X/BUCKETS)):



    plt.plot(range(0,X), temps)
    plt.plot(range(0,X), commits)
    plt.show()
if __name__ == '__main__':
    main()
