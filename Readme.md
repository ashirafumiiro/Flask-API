# Flask API 

This implements a flask API with Crud operations and endpoints shown below.  
  
`-/create`  
Create odds.   
Accepts json with the following fields:   
league, home_team, away_team, home_team_win_odds, away_team_win_odds, draw_odds, game_date and saves this into a database  
Returns:   
- 200 if it succeeds
- 500 for server error
- 403 for incorrect request. For a 403 response, return a json with a details field that contains information on what is wrong with the request
-/read

Read game odds.   
Accepts json with the following fields: 
league, date_range  
Returns: 
- 200 if it succeeds. For a 200 response, return a json array with odds for that whole league for the specified date range
- 500 for server error.
- 403 for incorrect request. For a 403 response, return a json with a details field that contains information on what is wrong with the request

`-/update` 

Update game odds.
Accepts json with the following fields: 
league, home_team, away_team, home_team_win_odds, away_team_win_odds, draw_odds, game_date and saves this into a database  
Returns:
- 200 if it succeeds
- 500 for server error
- 403 for incorrect request. For a 403 response, return a json with a details field that contains information on what is wrong with the request

`-/delete`

Delete game odds.
Accepts json with the following fields: 
league, home_team, away_team and game_date and deletes this from the database  
Returns: 
- 200 if it succeeds
- 500 for server error
- 403 for incorrect request. For a 403 response, return a json with a details field that contains information on what is wrong with the request  
## Badges
[![Build Status](https://travis-ci.com/ashirafumiiro/Flask-API.svg?branch=master)](https://travis-ci.com/ashirafumiiro/Flask-API)  
[![codecov](https://codecov.io/gh/ashirafumiiro/Flask-API/branch/master/graph/badge.svg)](https://codecov.io/gh/ashirafumiiro/Flask-API)

