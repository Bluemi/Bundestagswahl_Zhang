from engine_session import create_session, State, Constituency
from flask import Flask, jsonify, abort, render_template, Response
app = Flask(__name__)

db_session = create_session()


@app.route('/<name>')
def start_page(name):
    return render_template(name);


@app.route('/states')
def get_states():
    states = list(map(lambda state: {'id': state.id, 'name': state.name}, db_session.query(State).all()))
    return jsonify(states)


@app.route('/constituencies/<state_id>')
def get_constituencies(state_id):
    state = db_session.query(State).filter(State.id == state_id).first()

    if state:
        constituencies = list(map(lambda c: {'id': c.id, 'name': c.name}, state.constituencies))
        return jsonify(constituencies)
    else:
        abort(404)


@app.route('/votes/<constituency_id>')
def get_votes(constituency_id):
    constituency = db_session.query(Constituency).filter(Constituency.id == constituency_id).first()

    if constituency:
        votes = constituency.votes
        votes = map(
            lambda vote: {'party': vote.party.name,
                          'first_vote': vote.first_vote,
                          'second_vote': vote.second_vote},
            votes
        )
        return jsonify(list(votes))
    else:
        abort(404)


app.run(debug=True, port=5000)
