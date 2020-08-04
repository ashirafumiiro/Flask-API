from flask import Flask, request, jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy
import os
from flask_marshmallow import Marshmallow
from functools import wraps
import datetime

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ma = Marshmallow(app)


class Odd(db.Model):
    __tablename__ = 'odd'
    id = db.Column(db.Integer, primary_key=True)
    league = db.Column(db.String(80), nullable=False)
    home_team = db.Column(db.String(80), nullable=False) 
    away_team = db.Column(db.String(80), nullable=False) 
    home_team_win_odds = db.Column(db.Float, nullable=False)
    away_team_win_odds = db.Column(db.Float, nullable=False)
    draw_odds = db.Column(db.Float, nullable=False) 
    game_date = db.Column(db.Date, nullable=False)

    def __init__(self, leage, home_team, away_team, home_team_win_odds, away_team_win_odds,
                    draw_odds, game_date):
        self.league = leage
        self.home_team = home_team
        self.away_team = away_team
        self.home_team_win_odds = home_team_win_odds
        self.away_team_win_odds = away_team_win_odds
        self.draw_odds = draw_odds
        self.game_date = game_date

    def __repr__(self):
        return '<Odd %r vs %r>' % (self.home_team, self.away_team)


# Odd Schema
class OddSchema(ma.Schema):
    class Meta:
        fields =  ('id', 'league', 'home_team', 'away_team', 'home_team_win_odds', 
                    'away_team_win_odds', 'draw_odds', 'game_date')  


#init Schema
odd_schema = OddSchema()
odds_schema = OddSchema(many=True)


def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        with open('api.key', 'r') as apikey:
            key=apikey.read().replace('\n', '')
        #if request.args.get('key') and request.args.get('key') == key:
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == key:
            return view_function(*args, **kwargs)
        else:
            abort(make_response(jsonify(message="Valid Api key required"), 403))
    return decorated_function


# Create
@app.route('/create', methods=['POST'])
@require_appkey
def add_odd():
    try:
        league = request.json['league'] 
        home_team = request.json['home_team'] 
        away_team = request.json['away_team'] 
        home_team_win_odds = request.json['home_team_win_odds'] 
        away_team_win_odds = request.json['away_team_win_odds'] 
        draw_odds = request.json['draw_odds'] 
        game_date = request.json['game_date']
        date = datetime.datetime.strptime(game_date, "%Y-%m-%d").date()

        new_odd = Odd(league, home_team, away_team, home_team_win_odds, away_team_win_odds,
                        draw_odds, date)
        db.session.add(new_odd)
        db.session.commit()
        return odd_schema.jsonify(new_odd)
    except Exception:  # All other exception taken to be server error
        return '', 500
    


# Get odds
@app.route('/read', methods=['POST'])
@require_appkey
def get_odds():
    try:
        league = request.json['league'] 
        date_range = request.json['date_range'] # assume to be array of [from_date, to_date]
        from_date = datetime.datetime.strptime(date_range[0], "%Y-%m-%d").date()
        to_date = datetime.datetime.strptime(date_range[1], "%Y-%m-%d").date()

        odds = Odd.query.filter_by(league=league).filter(Odd.game_date>=from_date).filter(Odd.game_date<=to_date)
        results = odds_schema.dump(odds)
        return jsonify(results)
    except Exception:  # internal server errors
        return '', 500

#update
@app.route('/update/<id>', methods=['PUT'])
@require_appkey
def update_odd(id):
    try:
        odd = Odd.query.get(id)
        if not odd:
            return '', 404

        league = request.json['league'] 
        home_team = request.json['home_team'] 
        away_team = request.json['away_team'] 
        home_team_win_odds = request.json['home_team_win_odds'] 
        away_team_win_odds = request.json['away_team_win_odds'] 
        draw_odds = request.json['draw_odds'] 
        game_date = request.json['game_date']
        date = datetime.datetime.strptime(game_date, "%Y-%m-%d").date()
        
        odd.leage = league
        odd.home_team = home_team
        odd.away_team = away_team
        odd.home_team_win_odds = home_team_win_odds
        odd.away_team_win_odds = away_team_win_odds
        odd.draw_odds = draw_odds
        odd.game_date = date

        db.session.commit()

        return odd_schema.jsonify(odd)
    except Exception: # internal server errors
        return '', 500

# Delete Odd
@app.route('/delete', methods=['DELETE'])
@require_appkey
def delete_odd():
    try:
        league = request.json['league'] 
        home_team = request.json['home_team'] 
        away_team = request.json['away_team'] 
        game_date = request.json['game_date']
        game_date = datetime.datetime.strptime(game_date, "%Y-%m-%d").date()

        odd_to_delete = Odd.query.filter_by(league=league, home_team=home_team, 
                                                away_team=away_team, game_date=game_date).first()
        if not odd_to_delete:
            return '', 404
        db.session.delete(odd_to_delete)
        db.session.commit()
        return odd_schema.jsonify(odd_to_delete)
    except Exception:
        raise Exception
        return '', 500
        

if __name__ == "__main__":
    app.run(debug=True)
