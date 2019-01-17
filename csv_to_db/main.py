from parser import pandas_frame_from_csv_path, get_states, get_constituency_of
from engine_session import create_engine_session, State, Constituency, Party, Vote


def main():
    engine, session = create_engine_session()

    frame = pandas_frame_from_csv_path('../btw17_kerg.csv', lines_to_skip=2, sep=';')

    add_states(get_states(frame), session)
    add_constituencies(frame, session)
    add_parties(frame, session)
    add_votes(frame, session)

    # print(session.query(Constituency).filter_by(name='Hamburg-Wandsbek').first().state)


def add_states(states, session):
    """
    Adds the states given in a pandas frame to the current session.

    :param states: The states to add to the current session.
    :param session: The current sqlalchemy session.
    """

    for state_name in states['Gebiet']:
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

    for state_nr, state_name in zip(states['Nr'], states['Gebiet']):
        db_state = session.query(State).filter_by(name=state_name).first()

        constituency = get_constituency_of(frame, state_nr)

        for constituency_name in constituency['Gebiet']:
            db_constituency = Constituency(name=constituency_name, state=db_state)
            session.add(db_constituency)


def add_parties(frame, session):
    """
    Adds the parties given in frame to session.

    :param frame: The pandas frame from where to extract the parties.
    :param session: The current sqlalchemy session
    """
    # magic: Cuts away NaN Values and unneeded information
    parties = frame.iloc[0][19:].index[0::4][:-2]

    for party_name in parties:
        db_party = Party(name=party_name)
        session.add(db_party)


def get_votes(frame, party, constituency):
    """
    Extracts the first and second vote of the given party in the given constituency as tuple.

    :param frame: The pandas frame from where to extract the votes.
    :param party: The given party
    :param constituency: The given constituency
    :return: (first_voice, second_voice)
    """
    print(frame[party.name])
    raise NotImplementedError


def add_votes(frame, session):
    """
    Adds the votes given in frame to session.

    :param frame: The pandas frame from where to extract the votes.
    :param session: The current sqlalchemy session
    """
    constituencies = session.query(Constituency).all()
    parties = session.query(Party).all()

    for party in parties:
        for constituency in constituencies:
            first_votes, second_votes = get_votes(frame, party, constituency)
            db_vote = Vote(first_vote=first_votes, second_vote=second_votes, constituency=constituency, party=party)
            session.add(db_vote)

    session.commit()


if __name__ == '__main__':
    main()
