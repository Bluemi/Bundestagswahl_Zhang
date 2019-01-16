import sqlalchemy
from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class State(Base):
    """
    Represents one state.
    """
    __tablename__ = 'states'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # constituency relation
    constituencies = relationship('Constituency', back_populates='state')

    def __repr__(self):
        return 'State: id={id}, name={name}'.format(id=self.id, name=self.name)


class Vote(Base):
    """
    Represents the number of first/second votes for one party in one constituency.
    """
    __tablename__ = 'votes'

    # foreign keys
    constituency_id = Column(Integer, ForeignKey('constituencies.id'), primary_key=True)
    party_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)

    # vote data
    first_vote = Column(Integer)
    second_vote = Column(Integer)

    # relations
    constituency = relationship('Constituency', back_populates='party')
    party = relationship('Party', back_populates='constituency')


class Constituency(Base):
    """
    Represents a constituency.
    Each constituency has exactly one state to which it belongs.
    A constituency has a vote for every party.
    """
    __tablename__ = 'constituencies'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    first_vote = Column(Integer)
    second_vote = Column(Integer)

    # state relation
    state_id = Column(Integer, ForeignKey('states.id'))
    state = relationship('State', back_populates='constituencies')

    # vote/party relation
    party = relationship('Vote', back_populates='constituency')


class Party(Base):
    """
    Represents a party. A party has a vote for every constituency.
    """
    __tablename__ = 'parties'

    id = Column(Integer, primary_key=True)

    name = Column(String)

    # vote/constituency relation
    constituency = relationship('Vote', back_populates='party')


def create_engine_session():
    engine = sqlalchemy.create_engine('sqlite:///:memory:')
    Session = sessionmaker()
    Session.configure(bind=engine)

    session = Session()

    State.metadata.create_all(engine)
    Constituency.metadata.create_all(engine)
    Vote.metadata.create_all(engine)
    Party.metadata.create_all(engine)
    Base.metadata.create_all(engine)

    return engine, session
