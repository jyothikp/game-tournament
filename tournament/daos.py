import pymongo
from pymongo import IndexModel
from tournament.data_store import DataStore
from tournament.utils import Singleton


class TournamentDAO(DataStore):
    __metaclass__ = Singleton

    index_1 = IndexModel([('tournament_id', pymongo.ASCENDING)], unique=True, sparse=True)
    index_2 = IndexModel([('name', pymongo.ASCENDING)], unique=True)

    def __init__(self):
        super().__init__('Tournament')
        self._create_indexes([self.index_1, self.index_2])


class TitleDAO(DataStore):
    __metaclass__ = Singleton

    index_1 = IndexModel([('title', pymongo.ASCENDING)], unique=True)

    def __init__(self):
        super().__init__('Title')
        self._create_indexes([self.index_1])


class MatchDAO(DataStore):
    __metaclass__ = Singleton

    # Possible unique key constraint on external match_id
    def __init__(self):
        super().__init__('Match')


class ScoresDAO(DataStore):
    __metaclass__ = Singleton

    def __init__(self):
        super().__init__('Scores')


class TeamsDAO(DataStore):
    __metaclass__ = Singleton
    index_1 = IndexModel([('team_id', pymongo.ASCENDING)], unique=True)

    def __init__(self):
        super().__init__('Teams')
        self._create_indexes([self.index_1])


class ParticipantsDAO(DataStore):
    __metaclass__ = Singleton

    def __init__(self):
        super().__init__('Participants')


class EventMetaDAO(DataStore):
    __metaclass__ = Singleton

    index_1 = IndexModel([('match_id', pymongo.ASCENDING)], unique=True)

    def __init__(self):
        super().__init__('EventMeta')
        self._create_indexes([self.index_1])
