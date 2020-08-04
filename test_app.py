import os
import json
import tempfile

import pytest

import app

headers = {'Content-Type':'application/json', 'x-api-key': '1234567890'}
test_data = {
    "league" :  "FA",
    "home_team": "Arsenal", 
    "away_team": "Man City", 
    "home_team_win_odds": 3.0, 
    "away_team_win_odds": 4, 
    "draw_odds": 2, 
    "game_date": "2020-02-19" 
}
@pytest.fixture
def client():
    db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
    app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+app.app.config['DATABASE']
    app.app.config['TESTING'] = True
    client = app.app.test_client()

    with app.app.app_context():
        app.db.create_all()

    yield client

    os.close(db_fd)
    os.unlink(app.app.config['DATABASE'])


# Test create   #######################################
def test_create_without_key(client):

    rv = client.post('/create', json=test_data)
    json_data = rv.get_json()
    
    assert json_data['message'] == 'Valid Api key required'
    assert rv.status_code == 403


def test_create_with_key(client):
    rv = client.post('/create', headers=headers,
                        json=test_data)
    json_data = rv.get_json()
    assert json_data['id'] > 0
    assert rv.status_code == 200


def test_create_with_key_500(client):
    data = {
        "league" :  "FA",
        "home_team": "Arsenal", 
        "away_team": "Man City", 
        "home_team_win_odds": 3.0, 
        "away_team_win_odds": 4, 
        "draw_odds": 2, 
        "game_dates_wrong": "2020-02-18" #wrong data
    }
    rv = client.post('/create', headers=headers,
                        json=data,)
    
    assert rv.status_code == 500


# Test update #############################
def test_update_without_key(client):
    data = {
        "league" :  "FA",
        "home_team": "Arsenal", 
        "away_team": "Man City", 
        "home_team_win_odds": 3.0, 
        "away_team_win_odds": 7, 
        "draw_odds": 2, 
        "game_date": "2020-02-19" 
    }
    rv = client.put('/update/1', json=data)
    json_data = rv.get_json()

    assert json_data['message'] == 'Valid Api key required'
    assert rv.status_code == 403


def test_update_with_key(client):
    data = {
        "league" :  "FA",
        "home_team": "Arsenal", 
        "away_team": "Man City", 
        "home_team_win_odds": 3.0, 
        "away_team_win_odds": 4, 
        "draw_odds": 2, 
        "game_date": "2020-02-19",
    }
    rv1 = client.post('/create', headers=headers, json=test_data)  # Create it
    assert rv1.status_code == 200
    rv = client.put('/update/1', headers=headers,
                        json=data,)
    assert rv.status_code == 200 
    rv = client.put('/update/3', headers=headers, json=data)  # non existing
    assert rv.status_code == 404 

def test_update_with_key_500(client):
    data = {
        "league" :  "FA",
        "home_team": "Arsenal", 
        "away_team": "Man City", 
        "home_team_win_odds": 3.0, 
        "away_team_win_odds": 4, 
        "draw_odds": 2, 
        "game_dates_wrong": "2020-02-18" # error in this parameter
    }
    
    rv = client.put('/update/1', headers=headers,
                        json=data,)
    
    assert rv.status_code == 500


# Test Read  #############################
def test_read_without_key(client):
    data = {
        "league" :  "FA",
        "date_range": ["2020-02-18", "2020-02-18"]
    }
    rv = client.post('/read', json=data)
    json_data = rv.get_json()

    assert json_data['message'] == 'Valid Api key required'
    assert rv.status_code == 403


def test_read_with_key(client):
    data = {
        "league": "FA",
        "date_range": ["2020-01-18", "2020-02-3"]
    }
    rv = client.post('/read', json=data, headers=headers)
    json_data = rv.get_json()
    assert rv.status_code == 200


def test_read_with_key_500(client):
    data = {
        "league": "FA",
        "date_ranges_WRONG": ["2020-01-18", "2020-02-3"] # wrong param
    }
    rv = client.post('/read', json=data, headers=headers)
    json_data = rv.get_json()
    assert rv.status_code == 500


# Test Delete
def test_delete_without_key(client):
    data = {
        "league" :  "FA",
        "home_team": "Arsenal", 
        "away_team": "Man City", 
        "game_date": "2020-02-19"
    }
    
    rv = client.delete('/delete', json=test_data)
    json_data = rv.get_json()

    assert json_data['message'] == 'Valid Api key required'
    assert rv.status_code == 403

def test_delete_with_key(client):
    data = {
        "league" :  "FA",
        "home_team": "Arsenal", 
        "away_team": "Man City", 
        "game_date": "2020-02-19"
    }
    rv1 = client.post('/create', headers=headers, json=test_data)  # Create it
    assert rv1.status_code == 200
    rv = client.delete('/delete', json=data, headers=headers)  # Delete it
    assert rv.status_code == 200
    rv = client.delete('/delete', json=data, headers=headers)  # Delete it
    assert rv.status_code == 404 # now it's not there

def test_delete_with_key_500(client):
    data = {
        "league" :  "FA",
        "home_team": "Arsenal", 
        "away_team": "Man City", 
        "game_date_wrong": "2020-02-19"  # wrong param
    }
    rv = client.delete('/delete', json=data, headers=headers)
    assert rv.status_code == 500