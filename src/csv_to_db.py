import math

from parser import pandas_frame_from_csv_path, get_states, get_constituency_of, normalize_data_frame
from engine_session import create_session, State, Constituency, Party, Vote
from tqdm import tqdm


def main():
    session = create_session()

    frame = pandas_frame_from_csv_path('btw17_kerg.csv', lines_to_skip=2, sep=';')
    # normalize_data_frame(frame)

    add_states(get_states(frame), session)
    add_constituencies(frame, session)
    add_parties(frame, session)

    add_votes(frame, session)


def add_states(states, session):
    """
    Adds the states given in a pandas frame to the current session.

    :param states: The states to add to the current session.
    :param session: The current sqlalchemy session.
    """

    for state_name in tqdm(states['Gebiet'], desc='adding states'):
        db_state = State(name=state_name)
        session.add(db_state)

    session.commit()


def add_constituencies(frame, session):
    """
    Adds the constituencies given in frame to session.

    :param frame: The pandas frame from where to extract the constituencies.
    :param session: The current sqlalchemy session
    """

    states = get_states(frame)

    for state_nr, state_name in tqdm(zip(states['Nr'], states['Gebiet']), desc='adding constituencies', total=16):
        db_state = session.query(State).filter_by(name=state_name).first()

        constituency = get_constituency_of(frame, state_nr)

        for constituency_name in constituency['Gebiet']:
            db_constituency = Constituency(name=constituency_name, state=db_state)
            session.add(db_constituency)

    session.commit()


def add_parties(frame, session):
    """
    Adds the parties given in frame to session.

    :param frame: The pandas frame from where to extract the parties.
    :param session: The current sqlalchemy session
    """
    # magic: Cuts away NaN Values and unneeded information
    parties = frame.iloc[0][19:].index[0::4][:-1]

    for party_name in tqdm(parties, desc='adding parties'):
        db_party = Party(name=party_name)
        session.add(db_party)

    session.commit()


def get_votes(frame, party, constituency):
    """
    Extracts the first and second vote of the given party in the given constituency as tuple.

    :param frame: The pandas frame from where to extract the votes.
    :param party: The given party
    :param constituency: The given constituency
    :return: (first_voice, second_voice)
    """
    new_frame = frame[frame['Gebiet'] == constituency.name].loc[:, party.name:]

    first_vote = new_frame.iloc[:, 0]
    second_vote = new_frame.iloc[:, 2]

    if math.isnan(first_vote):
        first_vote = 0
    if math.isnan(second_vote):
        second_vote = 0

    return int(first_vote), int(second_vote)


def add_votes(frame, session):
    """
    Adds the votes given in frame to session.

    :param frame: The pandas frame from where to extract the votes.
    :param session: The current sqlalchemy session
    """
    constituencies = session.query(Constituency).all()
    parties = session.query(Party).all()

    for party in tqdm(parties, desc='adding votes'):
        for constituency in constituencies:
            first_votes, second_votes = get_votes(frame, party, constituency)
            db_vote = Vote(first_vote=first_votes, second_vote=second_votes, constituency=constituency, party=party)
            session.add(db_vote)

    session.commit()


if __name__ == '__main__':
    main()
