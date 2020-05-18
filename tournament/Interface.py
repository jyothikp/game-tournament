from copy import deepcopy

from tournament.exceptions import InvalidDataException
from tournament.logger import Logger
from tournament.service import EventMetaService
from tournament.service import MatchDataService
from tournament.service import ParticipantsDataService
from tournament.service import ScoresDataService
from tournament.service import TeamsDataService
from tournament.service import TitleDataService
from tournament.service import TournamentDataService
from dateutil.parser import parse


class GameInterface:
    def __init__(self):
        self.data = None
        self.source = None

    def save(self, data):
        self.data = data.pop('data', {})
        self.source = data.get('source')
        if not self.data:
            raise InvalidDataException("Not data present")
        Logger().info("save_game_info", action='save_started', data=self.data, source=self.source)
        tournament_id = TournamentDataService().save(self.data.get('tournament'))
        title_id = TitleDataService().save({'title': self.data.get('title').strip()})

        match_data = dict(
                tournament_id=tournament_id,
                title_id=title_id,
                match_id=str(self.data.get('id')),
                url=self.data.get('url'),
                state=self.data.get('state'),
                best_of=self.data.get('bestof'),
                start_date=parse(self.data.get('date_start_text'), '')
        )
        match_id = MatchDataService().save(match_data)
        Logger().info("save_game_info", action='match_data_saved', match_data=match_data,
                      match_id=match_id)

        team_service = TeamsDataService()
        team_data = {}
        for team in self.data.get('teams', []):
            team_data[int(team.get('id', 0))] = team_service.save(team)

        participant_data = {'team_id_'+str(i+1): team_id for i, team_id in enumerate(team_data.values())}
        participant_data['match_id'] = match_id
        participant_id = ParticipantsDataService().save(participant_data)

        Logger().info("save_game_info", action='participant_data_saved', participant_data=participant_data,
                      participant_id=participant_id)

        # Possible exception handling for invalid team
        score_service = ScoresDataService()
        for score in self.data.get('scores', []):
            score_data = deepcopy(score)
            team_id = int(score_data.pop('team', 0))
            score_data['team_id'] = team_data[team_id]
            score_data['match_id'] = match_id
            score_service.save(score_data)

        event_id = EventMetaService().save({'source': self.source, 'match_id': match_id, 'raw_data': self.data})

        Logger().info("save_game_info", action='save_finished', event_id=event_id, match_id=match_id)

    def get_match(self, match_id):
        Logger().info("get_match_data", action="fetching_match_data_start", match_id=match_id)
        match = MatchDataService().find_by_id(match_id)
        event_data = EventMetaService().find_one({'match_id': match['id']})
        Logger().info("get_match_data", action="fetching_match_data_finished", match_id=match_id)
        return event_data['raw_data']

    def get_matches(self, query):
        match_query = {}
        if 'tournament' in query:
            tournament = TournamentDataService().find_one({'name': query['tournament']})
            if tournament is None:
                return {}
            match_query['tournament_id'] = tournament.id
        if 'title' in query:
            title = TitleDataService().find_one({'title': query['title']})
            if title is None:
                return {}
            match_query['title_id'] = title.id
        if 'state' in query:
            match_query['state'] = query['state']
        if 'date_start_gte' in query:
            match_query['start_date'] = {'$gte': parse(query['date_start_gte'])}
        if 'date_start_lte' in query:
            match_query['start_date'] = {'$lte': parse(query['date_start_lte'])}

        Logger().info("get_match_data", action="fetching_all_matches", query=match_query)
        matches = MatchDataService().find(match_query)
        data = []
        for match in matches:
            match_data = match.to_dict()
            query = {'match_id': match.id}
            match_data['scores'] = ScoresDataService().find(query, dict)
            participant = ParticipantsDataService().find_one(query)
            if participant is None:
                continue
            query = {'_id': {'$in': [participant.team_id_1, participant.team_id_2]}}
            match_data['teams'] = TeamsDataService().find(query, dict)
            data.append(match_data)
        Logger().info("get_match_data", action="fetched_all_data")
        return data
