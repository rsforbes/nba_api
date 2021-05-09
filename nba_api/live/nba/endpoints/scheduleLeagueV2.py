from nba_api.live.nba.endpoints._base import Endpoint
from nba_api.live.nba.library.http import NBALiveHTTP

class ScheduleLeagueV2(Endpoint):
    endpoint_url = 'scheduleLeagueV2.json'
    expected_data = {
  "meta": {
    "version": 1,
    "request": "http://nba.cloud/league/00/2020-21/scheduleleaguev2?Format=json",
    "time": "2021-05-08T20:33:05.335Z"
  },
  "leagueSchedule": {
    "seasonYear": "2020-21",
    "leagueId": "00",
    "gameDates":'12/11/2020 12:00:00 AM', 'games': [{'gameId': '0012000001', 'gameCode': '20201211/ORLATL', 'gameStatus': 3, 'gameStatusText': 'Final', 'gameSequence': 1, 'gameDateEst': '2020-12-11T00:00:00Z', 'gameTimeEst': '1900-01-01T19:00:00Z', 'gameDateTimeEst': '2020-12-11T19:00:00Z', 'gameDateUTC': '2020-12-11T05:00:00Z', 'gameTimeUTC': '1900-01-02T00:00:00Z', 'gameDateTimeUTC': '2020-12-12T00:00:00Z', 'awayTeamTime': '2020-12-11T19:00:00Z', 'homeTeamTime': '2020-12-11T19:00:00Z', 'day': 'Fri', 'monthNum': 12, 'weekNumber': 0, 'weekName': '', 'ifNecessary': False, 'seriesGameNumber': '', 'seriesText': '', 'arenaName': 'State Farm Arena', 'arenaState': 'GA', 'arenaCity': 'Atlanta', 'postponedStatus': 'A', 'broadcasters': {'nationalBroadcasters': [], 'homeTvBroadcasters': [{'broadcasterScope': 'home', 'broadcasterMedia': 'tv', 'broadcasterId': 1067, 'broadcasterDisplay': 'Fox Sports Southeast', 'broadcasterAbbreviation': 'FSSE-ATL', 'tapeDelayComments': ''}], 'homeRadioBroadcasters': [{'broadcasterScope': 'home', 'broadcasterMedia': 'radio', 'broadcasterId': 1491, 'broadcasterDisplay': 'WZGC 92.9 FM The Gam', 'broadcasterAbbreviation': 'WZGC', 'tapeDelayComments': ''}], 'awayTvBroadcasters': [], 'awayRadioBroadcasters': [{'broadcasterScope': 'away', 'broadcasterMedia': 'radio', 'broadcasterId': 1000273, 'broadcasterDisplay': 'WYGM 96.9FM / 740AM', 'broadcasterAbbreviation': 'WYGM-FM/AM', 'tapeDelayComments': ''}]}, 'homeTeam': {'teamId': 1610612737, 'teamName': 'Hawks', 'teamCity': 'Atlanta', 'teamTricode': 'ATL', 'teamSlug': 'hawks', 'wins': 0, 'losses': 1, 'score': 112, 'seed': 0}, 'awayTeam': {'teamId': 1610612753, 'teamName': 'Magic', 'teamCity': 'Orlando', 'teamTricode': 'ORL', 'teamSlug': 'magic', 'wins': 1, 'losses': 0, 'score': 116, 'seed': 0}, 'pointsLeaders': [{'personId': 202696, 'firstName': 'Nikola', 'lastName': 'Vucevic', 'teamId': 1610612753, 'teamCity': 'Orlando', 'teamName': 'Magic', 'teamTricode': 'ORL', 'points': 18.0}, {'personId': 1629631, 'firstName': "De'Andre", 'lastName': 'Hunter', 'teamId': 1610612737, 'teamCity': 'Atlanta', 'teamName': 'Hawks', 'teamTricode': 'ATL', 'points': 18.0}]}, {'gameId': '0012000002', 'gameCode': '20201211/NYKDET', 'gameStatus': 3, 'gameStatusText': 'Final', 'gameSequence': 2, 'gameDateEst': '2020-12-11T00:00:00Z', 'gameTimeEst': '1900-01-01T19:00:00Z', 'gameDateTimeEst': '2020-12-11T19:00:00Z', 'gameDateUTC': '2020-12-11T05:00:00Z', 'gameTimeUTC': '1900-01-02T00:00:00Z', 'gameDateTimeUTC': '2020-12-12T00:00:00Z', 'awayTeamTime': '2020-12-11T19:00:00Z', 'homeTeamTime': '2020-12-11T19:00:00Z', 'day': 'Fri', 'monthNum': 12, 'weekNumber': 0, 'weekName': '', 'ifNecessary': False, 'seriesGameNumber': '', 'seriesText': '', 'arenaName': 'Little Caesars Arena', 'arenaState': 'MI', 'arenaCity': 'Detroit', 'postponedStatus': 'A', 'broadcasters': {'nationalBroadcasters': [], 'homeTvBroadcasters': [{'broadcasterScope': 'home', 'broadcasterMedia': 'tv', 'broadcasterId': 135, 'broadcasterDisplay': 'Fox Sports Detroit', 'broadcasterAbbreviation': 'FSD', 'tapeDelayComments': ''}], 'homeRadioBroadcasters': [{'broadcasterScope': 'home', 'broadcasterMedia': 'radio', 'broadcasterId': 1188, 'broadcasterDisplay': '97.1 FM The Ticket', 'broadcasterAbbreviation': 'WXYT', 'tapeDelayComments': ''}], 'awayTvBroadcasters': [{'broadcasterScope': 'away', 'broadcasterMedia': 'tv', 'broadcasterId': 100, 'broadcasterDisplay': 'MSG', 'broadcasterAbbreviation': 'MSG', 'tapeDelayComments': ''}], 'awayRadioBroadcasters': [{'broadcasterScope': 'away', 'broadcasterMedia': 'radio', 'broadcasterId': 1023, 'broadcasterDisplay': 'ESPN NY 98.7', 'broadcasterAbbreviation': 'WEPN', 'tapeDelayComments': ''}]}, 'homeTeam': {'teamId': 1610612765, 'teamName': 'Pistons', 'teamCity': 'Detroit', 'teamTricode': 'DET', 'teamSlug': 'pistons', 'wins': 0, 'losses': 1, 'score': 84, 'seed': 0}, 'awayTeam': {'teamId': 1610612752, 'teamName': 'Knicks', 'teamCity': 'New York', 'teamTricode': 'NYK', 'teamSlug': 'knicks', 'wins': 1, 'losses': 0, 'score': 90, 'seed': 0}, 'pointsLeaders': [{'personId': 1629628, 'firstName': 'RJ', 'lastName': 'Barrett', 'teamId': 1610612752, 'teamCity': 'New York', 'teamName': 'Knicks', 'teamTricode': 'NYK', 'points': 15.0}]}, {'gameId': '0012000003', 'gameCode': '20201211/HOUCHI', 'gameStatus': 3, 'gameStatusText': 'Final', 'gameSequence': 3, 'gameDateEst': '2020-12-11T00:00:00Z', 'gameTimeEst': '1900-01-01T20:00:00Z', 'gameDateTimeEst': '2020-12-11T20:00:00Z', 'gameDateUTC': '2020-12-11T05:00:00Z', 'gameTimeUTC': '1900-01-02T01:00:00Z', 'gameDateTimeUTC': '2020-12-12T01:00:00Z', 'awayTeamTime': '2020-12-11T19:00:00Z', 'homeTeamTime': '2020-12-11T19:00:00Z', 'day': 'Fri', 'monthNum': 12, 'weekNumber': 0, 'weekName': '', 'ifNecessary': False, 'seriesGameNumber': '', 'seriesText': '', 'arenaName': 'United Center', 'arenaState': 'IL', 'arenaCity': 'Chicago', 'postponedStatus': 'A', 'broadcasters': {'nationalBroadcasters': [{'broadcasterScope': 'natl', 'broadcasterMedia': 'tv', 'broadcasterId': 7, 'broadcasterDisplay': 'NBA TV', 'broadcasterAbbreviation': 'NBA TV', 'tapeDelayComments': ''}], 'homeTvBroadcasters': [{'broadcasterScope': 'home', 'broadcasterMedia': 'tv', 'broadcasterId': 1656, 'broadcasterDisplay': 'NBC Sports Chicago', 'broadcasterAbbreviation': 'NBCSCH', 'tapeDelayComments': ''}], 'homeRadioBroadcasters': [{'broadcasterScope': 'home', 'broadcasterMedia': 'radio', 'broadcasterId': 1688, 'broadcasterDisplay': '670 AM / S: 1200 AM', 'broadcasterAbbreviation': 'WSCR/WRTO', 'tapeDelayComments': ''}], 'awayTvBroadcasters': [], 'awayRadioBroadcasters': [{'broadcasterScope': 'away', 'broadcasterMedia': 'radio', 'broadcasterId': 1000272, 'broadcasterDisplay': '790 AM / 740 AM', 'broadcasterAbbreviation': 'KBME/KTRH', 'tapeDelayComments': ''}]}, 'homeTeam': {'teamId': 1610612741, 'teamName': 'Bulls', 'teamCity': 'Chicago', 'teamTricode': 'CHI', 'teamSlug': 'bulls', 'wins': 0, 'losses': 1, 'score': 104, 'seed': 0}, 'awayTeam': {'teamId': 1610612745, 'teamName': 'Rockets', 'teamCity': 'Houston', 'teamTricode': 'HOU', 'teamSlug': 'rockets', 'wins': 1, 'losses': 0, 'score': 125, 'seed': 0}, 'pointsLeaders': [{'personId': 203998, 'firstName': 'Bruno', 'lastName': 'Caboclo', 'teamId': 1610612745, 'teamCity': 'Houston', 'teamName': 'Rockets', 'teamTricode': 'HOU', 'points': 17.0}]}, {'gameId': '0012000004', 'gameCode': '20201211/LACLAL', 'gameStatus': 3, 'gameStatusText': 'Final', 'gameSequence': 4, 'gameDateEst': '2020-12-11T00:00:00Z', 'gameTimeEst': '1900-01-01T22:00:00Z', 'gameDateTimeEst': '2020-12-11T22:00:00Z', 'gameDateUTC': '2020-12-11T05:00:00Z', 'gameTimeUTC': '1900-01-02T03:00:00Z', 'gameDateTimeUTC': '2020-12-12T03:00:00Z', 'awayTeamTime': '2020-12-11T19:00:00Z', 'homeTeamTime': '2020-12-11T19:00:00Z', 'day': 'Fri', 'monthNum': 12, 'weekNumber': 0, 'weekName': '', 'ifNecessary': False, 'seriesGameNumber': '', 'seriesText': '', 'arenaName': 'STAPLES Center', 'arenaState': 'CA', 'arenaCity': 'Los Angeles', 'postponedStatus': 'A', 'broadcasters': {'nationalBroadcasters': [], 'homeTvBroadcasters': [{'broadcasterScope': 'home', 'broadcasterMedia': 'tv', 'broadcasterId': 1651, 'broadcasterDisplay': 'Spectrum SportsNet', 'broadcasterAbbreviation': 'SPECSN', 'tapeDelayComments': ''}], 'homeRadioBroadcasters': [{'broadcasterScope': 'home', 'broadcasterMedia': 'radio', 'broadcasterId': 1095, 'broadcasterDisplay': 'ESPN LA 710', 'broadcasterAbbreviation': 'KSPN', 'tapeDelayComments': ''}], 'awayTvBroadcasters': [{'broadcasterScope': 'away', 'broadcasterMedia': 'tv', 'broadcasterId': 132, 'broadcasterDisplay': 'Fox Sports Prime Tic', 'broadcasterAbbreviation': 'FSPT', 'tapeDelayComments': ''}], 'awayRadioBroadcasters': [{'broadcasterScope': 'away', 'broadcasterMedia': 'radio', 'broadcasterId': 1022, 'broadcasterDisplay': 'AM 570 LA Sports', 'broadcasterAbbreviation': 'KLAC', 'tapeDelayComments': ''}]}, 'homeTeam': {'teamId': 1610612747, 'teamName': 'Lakers', 'teamCity': 'Los Angeles', 'teamTricode': 'LAL', 'teamSlug': 'lakers', 'wins': 1, 'losses': 0, 'score': 87, 'seed': 0}, 'awayTeam': {'teamId': 1610612746, 'teamName': 'Clippers', 'teamCity': 'LA', 'teamTricode': 'LAC', 'teamSlug': 'clippers', 'wins': 0, 'losses': 1, 'score': 81, 'seed': 0}, 'pointsLeaders': [{'personId': 1629659, 'firstName': 'Talen', 'lastName': 'Horton-Tucker', 'teamId': 1610612747, 'teamCity': 'Los Angeles', 'teamName': 'Lakers', 'teamTricode': 'LAL', 'points': 19.0}]}, {'gameId': '0012000005', 'gameCode': '20201211/SACPOR', 'gameStatus': 3, 'gameStatusText': 'Final', 'gameSequence': 5, 'gameDateEst': '2020-12-11T00:00:00Z', 'gameTimeEst': '1900-01-01T22:30:00Z', 'gameDateTimeEst': '2020-12-11T22:30:00Z', 'gameDateUTC': '2020-12-11T05:00:00Z', 'gameTimeUTC': '1900-01-02T03:30:00Z', 'gameDateTimeUTC': '2020-12-12T03:30:00Z', 'awayTeamTime': '2020-12-11T19:30:00Z', 'homeTeamTime': '2020-12-11T19:30:00Z', 'day': 'Fri', 'monthNum': 12, 'weekNumber': 0, 'weekName': '', 'ifNecessary': False, 'seriesGameNumber': '', 'seriesText': '', 'arenaName': 'Moda Center', 'arenaState': 'OR', 'arenaCity': 'Portland', 'postponedStatus': 'A', 'broadcasters': {'nationalBroadcasters': [{'broadcasterScope': 'natl', 'broadcasterMedia': 'tv', 'broadcasterId': 2, 'broadcasterDisplay': 'ESPN', 'broadcasterAbbreviation': 'ESPN', 'tapeDelayComments': ''}], 'homeTvBroadcasters': [{'broadcasterScope': 'home', 'broadcasterMedia': 'tv', 'broadcasterId': 1657, 'broadcasterDisplay': 'NBC Sports Northwest', 'broadcasterAbbreviation': 'NBCSNW', 'tapeDelayComments': ''}], 'homeRadioBroadcasters': [{'broadcasterScope': 'home', 'broadcasterMedia': 'radio', 'broadcasterId': 1472, 'broadcasterDisplay': 'Rip City Radio 620', 'broadcasterAbbreviation': 'KPOJ', 'tapeDelayComments': ''}], 'awayTvBroadcasters': [{'broadcasterScope': 'away', 'broadcasterMedia': 'tv', 'broadcasterId': 1027, 'broadcasterDisplay': 'NBC Sports Californi', 'broadcasterAbbreviation': 'NBCSCA', 'tapeDelayComments': ''}], 'awayRadioBroadcasters': [{'broadcasterScope': 'away', 'broadcasterMedia': 'radio', 'broadcasterId': 1052, 'broadcasterDisplay': 'KHTK Sports 1140 AM', 'broadcasterAbbreviation': 'KHTK', 'tapeDelayComments': ''}]}, 'homeTeam': {'teamId': 1610612757, 'teamName': 'Trail Blazers', 'teamCity': 'Portland', 'teamTricode': 'POR', 'teamSlug': 'blazers', 'wins': 1, 'losses': 0, 'score': 127, 'seed': 0}, 'awayTeam': {'teamId': 1610612758, 'teamName': 'Kings', 'teamCity': 'Sacramento', 'teamTricode': 'SAC', 'teamSlug': 'kings', 'wins': 0, 'losses': 1, 'score': 102, 'seed': 0}, 'pointsLeaders': [{'personId': 1627741, 'firstName': 'Buddy', 'lastName': 'Hield', 'teamId': 1610612758, 'teamCity': 'Sacramento', 'teamName': 'Kings', 'teamTricode': 'SAC', 'points': 23.0}]}]}
  }

    nba_response = None
    data_sets = None
    headers = None
    leagueSchedule = None


    def __init__(self,

                 proxy=None,
                 headers=None,
                 timeout=30,
                 get_request=True):
        self.proxy = proxy
        if headers is not None:
            self.headers = headers
        self.timeout = timeout

        if get_request:
            self.get_request()


    def get_request(self):
        nba_live = NBALiveHTTP()
        nba_live.base_url = 'https://cdn.nba.com/static/json/staticData/{endpoint}'
        self.nba_response = nba_live.send_api_request(
            endpoint=self.endpoint_url,
            parameters={},
            proxy=self.proxy,
            headers=self.headers,
            timeout=self.timeout
        )
        self.load_response()

    def load_response(self):
        data_sets = self.nba_response.get_dict()
        if 'leagueSchedule' in data_sets.keys():
            if 'gameDates' in data_sets['leagueSchedule']:
                self.leagueSchedule = Endpoint.DataSet(data=data_sets['leagueSchedule']['gameDates'])
                self.data_sets = [self.leagueSchedule]


