from copy import deepcopy

from pymongo.errors import DuplicateKeyError

from tournament.daos import EventMetaDAO
from tournament.daos import MatchDAO
from tournament.daos import ParticipantsDAO
from tournament.daos import ScoresDAO
from tournament.daos import TeamsDAO
from tournament.daos import TitleDAO
from tournament.daos import TournamentDAO
from tournament.models import EventMeta
from tournament.models import Match
from tournament.models import Participants
from tournament.models import Scores
from tournament.models import Teams
from tournament.models import Title
from tournament.models import Tournament


class BaseService:
    def __init__(self, model, dao):
        self.model = model
        self.dao = dao

    def save(self, data):
        try:
            return self.dao.save(self.model(**data))
        except DuplicateKeyError:
            return self.find_one(data).id

    def update_one(self, query, data):
        return self.dao.update_one(query, data)

    def find_one(self, query):
        data = self.dao.find_one(query)
        return self.model(**data) if data else None

    def find(self, query, model=None):
        model = self.model if model is None else model
        return [model(**data) for data in self.dao.find(query)]

    def find_by_id(self, obj_id):
        data = self.dao.find_by_id(obj_id)
        return self.model(**data) if data else None


class TournamentDataService(BaseService):
    def __init__(self):
        super().__init__(Tournament, TournamentDAO())

    def save(self, data):
        if isinstance(data, dict):
            data = dict(name=data.get('name').strip(), tournament_id=str(data.get('id')))
            query = dict(tournament_id=data['tournament_id'])
        else:
            data = dict(name=data)
            query = data

        return self.update_one(query, data)


class TitleDataService(BaseService):
    def __init__(self):
        super().__init__(Title, TitleDAO())


class MatchDataService(BaseService):
    def __init__(self):
        super().__init__(Match, MatchDAO())


class ScoresDataService(BaseService):
    def __init__(self):
        super().__init__(Scores, ScoresDAO())


class TeamsDataService(BaseService):
    def __init__(self):
        super().__init__(Teams, TeamsDAO())

    def save(self, data):
        data = deepcopy(data)
        team_id = int(data.pop('id', 0))
        query = dict(team_id=team_id)
        data['team_id'] = team_id
        return self.update_one(query, data)


class ParticipantsDataService(BaseService):
    def __init__(self):
        super().__init__(Participants, ParticipantsDAO())


class EventMetaService(BaseService):
    def __init__(self):
        super().__init__(EventMeta, EventMetaDAO())



