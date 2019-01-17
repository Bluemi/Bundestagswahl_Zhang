from parser import pandas_frame_from_csv_path, get_states, get_constituency_of
from engine_session import create_engine_session, State, Constituency


def main():
    engine, session = create_engine_session()

    frame = pandas_frame_from_csv_path('../btw17_kerg.csv', lines_to_skip=2, sep=';')

    add_states(get_states(frame), session)
    add_constituencies(frame, session)


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


if __name__ == '__main__':
    main()
