#!/usr/bin/env python

import csv
import json
import sys
import os

import pandas as pd

DEBUG = False
BASE_DATADIR = 'datasets'
DATADIR = '2022ey'
DEFAULT_COLUMNS = []

def parse_team_info(filename=f'{DATADIR}/team.csv'):
    return list(csv.DictReader(open(filename)))

def get_reviewer(email, team_info=None):
    if team_info is None:
        team_info = parse_team_info()
    try:
        return [item for item in team_info if item['email'] == email][0]
    except IndexError:
        raise Exception(f'ERROR: No reviewer found for {email}')

def calculate_matches(dataset):
    # Have to create the column, so that we can then limit the transform to _just_ that column
    dataset['matches'] = 0
    dataset['matches'] = dataset.groupby(['capability','performance'])['matches'].transform('count')
    # Here we are just adding a new column without transforming so can just set it directly.
    # we do this calculation just so that the graph looks prettier
    dataset['size'] = dataset['matches'] * 5

    return dataset

def average_dataset(dataset):
    mean = dataset.mean(numeric_only=True).round(0)
    dataset = pd.concat([dataset, pd.DataFrame([mean])], ignore_index=True)
    dataset = dataset.fillna('Average')
    return dataset

def get_dataset(employee, groupby):
    alldata = pd.read_json(json.dumps(parse_ratings()))
    tablecolumns = ['capability','performance']
    if employee == 'all':
        groupby = 'employee'
        tablecolumns.insert(0, groupby)
        dataset = alldata[tablecolumns].groupby(groupby).mean().round(0)
        dataset.reset_index(inplace=True)
    else:
        tablecolumns.insert(0, groupby)
        dataset = alldata[alldata['employee_initials'] == employee]
        dataset = average_dataset(dataset)
    dataset = calculate_matches(dataset)
    dataset = dataset.sort_values(by=tablecolumns)
    return (dataset, groupby, tablecolumns)

def parse_ratings_from_row(rowdata, team_info=None):
    if team_info is None:
        team_info = parse_team_info()
    ratings = []

    try:
        reviewer = get_reviewer(rowdata['Email Address'], team_info)
    except IndexError:
        sys.stderr.write(f'ERROR: No reviewer found for {rowdata["Email Address"]}')
    if DEBUG:
        print(f'Parsing row for reviewer {reviewer["name"]}')
    for employee in team_info:
        initials = employee['initials'].upper()
        capability = rowdata.get(f'{initials} - Capability')
        performance = rowdata.get(f'{initials} - Performance')
        #print(f'{initials} - {capability} - {performance} -')
        if capability and performance:
            role = reviewer['role']
            if reviewer['name'] == employee['name']:
                role = 'Self'
            ratings.append({
                'reviewer': reviewer['name'],
                'title': reviewer['title'],
                'role': role,
                'team': reviewer['team'],
                'employee': employee['name'],
                'employee_initials': initials,
                'capability': int(capability),
                'performance': int(performance),
                })
    if DEBUG:
        print(f'Found {len(ratings)} for {reviewer["name"]}')
    return ratings

def parse_ratings(filename=f'{DATADIR}/all.csv'):
    ratings = []

    for row in csv.DictReader(open(filename)):
        ratings.extend(parse_ratings_from_row(row))

    return ratings

