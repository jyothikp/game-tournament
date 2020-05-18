from enum import Enum

from bson import ObjectId


class StringEnum(Enum):

    @classmethod
    def from_str(cls, value, default=None):
        return cls._value2member_map_.get(value, default)

    def __str__(self):
        return self.value


class Services(StringEnum):
    MESSAGE_BROKER = 'rabbit_mq'
    DATABASE = 'mongodb'


class Document(object):
    def __init__(self, **kwargs):
        self._id = None
        kwargs['_id'] = kwargs['_id'] if kwargs.get('_id') else ObjectId()
        for key in self.__dict__:
            self.__setattr__(key, kwargs.get(key))

    def to_dict(self):
        return self.__dict__

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def __iter__(self):
        for key in self.__dict__:
            yield key

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value


class Tournament(Document):
    def __init__(self, **kwargs):
        self.name = None
        self.tournament_id = None
        super(Tournament, self).__init__(**kwargs)


class Title(Document):
    def __init__(self, **kwargs):
        self.title = None
        super(Title, self).__init__(**kwargs)


class Match(Document):
    def __init__(self, **kwargs):
        self.match_id = None
        self.url = None
        self.state = None
        self.best_of = None
        self.start_date = None
        self.title_id = None
        self.tournament_id = None
        super(Match, self).__init__(**kwargs)


class Teams(Document):
    def __init__(self, **kwargs):
        self.team_id = None
        self.name = None
        super(Teams, self).__init__(**kwargs)


class Scores(Document):
    def __init__(self, **kwargs):
        self.team_id = None
        self.score = None
        self.match_id = None
        self.winner = None
        super(Scores, self).__init__(**kwargs)


class Participants(Document):
    def __init__(self, **kwargs):
        self.team_id_1 = None
        self.team_id_2 = None
        self.match_id = None

        super().__init__(**kwargs)


class EventMeta(Document):
    def __init__(self, **kwargs):
        self.source = None
        self.match_id = None
        self.raw_data = None
        super(EventMeta, self).__init__(**kwargs)
