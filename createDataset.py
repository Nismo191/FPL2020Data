import json
import os
import sqlite3
import requests

from collections import OrderedDict

import tables as tables

def main(page):
    team_ids = []
    leagueStandings = requests.get(f'https://fantasy.premierleague.com/api/leagues-classic/314/standings/?page_new_entries=1&page_standings={str(page)}')
    jsonData = leagueStandings.json()
    leagueStandingsJson = jsonData["standings"]["results"]
    for entry in leagueStandingsJson:
            team_ids.append(str(entry["entry"]))

    create_leaguestandings(conn, leagueStandingsJson)

    for id in team_ids:
        teamResults = requests.get(f'https://fantasy.premierleague.com/api/entry/{id}/history/')
        jsonData = teamResults.json()
        teamResultsJson = jsonData["current"]
        for i in teamResultsJson:
            i.update({"id":int(id)})
        create_teamResults(conn, teamResultsJson)




db_file = database_file = 'fpl_all.sqlite'
conn = sqlite3.connect(db_file)

def create_leaguestandings(conn, data, table_name='entries'):
    column_constraints = {
        'id': 'primary key'
    }

    with conn:
        schema = tables.generate_table_schema(data, column_constraints=column_constraints)
        tables.create_table(conn, schema, table_name)
        tables.populate_table(conn, schema, table_name, data)


def create_teamResults(conn, data, table_name='team_results'):
    column_constraints = {
        'event': 'id'
    }

    with conn:
        schema = tables.generate_table_schema(data)
        tables.create_table(conn, schema, table_name)
        tables.populate_table(conn, schema, table_name, data)


if __name__ == "__main__":
    for i in range(142, 201):
        print(str(i))
        main(i)




