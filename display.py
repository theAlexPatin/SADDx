import json
import datetime
import matplotlib.pyplot as plt
import numpy as np
import math

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
    BUCKET_SIZE=25
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

    commit_buckets = list()
    temp_buckets = list()
    bucket_total = 0
    commit_total = 0
    for i in range(0, math.floor(X / BUCKET_SIZE)):
        commit_total = 0
        temp_total = 0
        for j in range(0, BUCKET_SIZE):
            commit_total += commits[i * BUCKET_SIZE + j]
            temp_total += temps[i * BUCKET_SIZE + j]
        commit_buckets.append(commit_total / BUCKET_SIZE)
        temp_buckets.append(temp_total / BUCKET_SIZE)
    plt.plot(range(0,math.floor(X / BUCKET_SIZE)), temp_buckets)
    plt.plot(range(0,math.floor(X / BUCKET_SIZE)), commit_buckets)
    plt.gca().legend(('Temperature in Boston', "Alex's git commits"))
    plt.title("Alex's Productivity vs. Temperature in Boston")
    plt.xlabel('Time (Sept 2018 - Sept 2019)')
    plt.show()
if __name__ == '__main__':
    main()
