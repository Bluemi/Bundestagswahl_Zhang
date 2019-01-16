from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

# Global Variables
SQLITE = 'sqlite'

# Table Names
COUNTRY = 'Bundesländer'
CONSTITUENCY = 'Wahlkreise'
GROUP = 'Parteien'
VOTE = 'Stimmen'

class MyDatabase:
    DB_Engine = {
        SQLITE: 'sqlite'
}