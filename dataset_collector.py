import requests
import json
import time
import random
import sys


class Player:
    name = ""
    id = ""
    puuid = ""
    champion_name = ""
    champion_id = -1
    spell1id = -1
    spell2id = -1
    summoner_level = -1
    rank = ""

    def __init__(self, name, id, rank):
        self.name = name.encode('utf-8')
        self.id = id
        self.rank = rank

    def __str__(self):
        return "%s,%s,%s,%d,%d,%d,%d" % \
               (self.name, self.rank, self.champion_name, self.champion_id,
                self.spell1id, self.spell2id, self.summoner_level)


class Match:
    raw = ""
    winners = []
    losers = []
    match_id = ""
    win = False

    def __init__(self, raw):
        self.raw = raw
        self.win = random.randint(0, 1) == 0
        self.winners = []
        self.losers = []
        self.match_id = ""

    def add_winner(self, winner_json):
        self.winners.append(winner_json)

    def add_lose(self, loser_json):
        self.losers.append(loser_json)

    def process(self):
        self.match_id = self.raw['metadata']['matchId']

        for play in self.raw['info']['participants']:
            p = Player(play['summonerName'], play['summonerId'], "placehold")
            p.puuid = play['puuid']
            p.champion_id = play['championId']
            p.champion_name = play['championName']
            p.spell1id = play['summoner1Id']
            p.spell2id = play['summoner2Id']
            p.summoner_level = play['summonerLevel']

            if play['win']:
                self.winners.append(p)
            else:
                self.losers.append(p)

    def __str__(self):
        s = "%s" % self.match_id
        if self.win:
            for play in self.winners:
                s = "%s,%s" % (s, str(play))
            for play in self.losers:
                s = "%s,%s" % (s, str(play))
        else:
            for play in self.losers:
                s = "%s,%s" % (s, str(play))
            for play in self.winners:
                s = "%s,%s" % (s, str(play))
        s = ("%s,1" if self.win else "%s,0") % s
        return "%s" % s


def get_header():
    header = "MATCH_ID"

    for i in range(1, 11):
        player_header = "P%dNAME,P%dRANK,P%dCHAMPION,P%dCHAMPIONID,P%dSPELL1,P%dSPELL2,P%dSUMMONERLEVEL" \
                        % (i, i, i, i, i, i, i)
        header += ",%s" % player_header

    header += ",WIN"

    return header


def request_until_success(request_url):
    success = False
    response = ""
    while not success:
        print("Sending request for %s." % request_url)
        response = requests.get(request_url)
        if response.status_code == 401 or response.status_code == 403:
            print("Response %d - Go regenerate API key. Killing." % response.status_code)
            assert False
        elif response.status_code == 429:
            sleeptime = int(response.headers["Retry-After"])
            print("Response %d - rate limit hit. Sleeping for %d and retrying later." % (response.status_code, sleeptime))
            time.sleep(sleeptime)
        elif response.status_code != 200:
            print("Response %d. Unexpected. Killing." % response.status_code)
            assert False
        else:
            success = True
    assert response.status_code == 200  # sanity check
    return response


def get_match(match_id):
    print("Fetching match with match id %s." % match_id)
    url = "https://americas.api.riotgames.com/lol/match/v5/matches/%s?api_key=%s" % (match_id, api_key)
    response = request_until_success(url)
    return json.loads(response.text)


def get_matches(puuid):
    print("Fetching match data for player with puuid %s." % puuid)
    url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" \
          "%s/ids?start=0&count=20&api_key=%s" % (puuid, api_key)
    response = request_until_success(url)
    return json.loads(response.text)


def get_summoner(summoner_id):
    print("Fetching puuid for player with summoner id %s." % summoner_id)
    url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/%s?api_key=%s" % (summoner_id, api_key)
    response = request_until_success(url)
    return json.loads(response.text)


def get_league(tier, division):
    url = ""
    # different apis for grandmaster, master, and challenger league... thanks Riot
    if tier == "GRANDMASTER":
        url = "https://na1.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/" \
              "RANKED_SOLO_5x5?api_key=%s" % api_key
    elif tier == "MASTER":
        url = "https://na1.api.riotgames.com/lol/league/v4/masterleagues/by-queue/" \
              "RANKED_SOLO_5x5?api_key=%s" % api_key
    elif tier == "CHALLENGER":
        url = "https://na1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/" \
              "RANKED_SOLO_5x5?api_key=%s" % api_key
    else:
        url = "https://na1.api.riotgames.com/lol/league/v4/entries/" \
              "RANKED_SOLO_5x5/%s/%s?page=1&api_key=%s" % (tier, division, api_key)
    response = request_until_success(url)
    return json.loads(response.text)


def print_json(d):
    print(json.dumps(d, indent=4))


def format_json(d):
    return json.dumps(d, indent=4)


def collect_players():
    tiers = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND", "MASTER", "GRANDMASTER", "CHALLENGER"]
    divisions = ["I", "II", "III", "IV"]

    player_list = []

    # get a player from each league
    for tier in tiers:
        r = ""
        print("Requesting players from tier %s." % tier)
        if tier == "MASTER" or tier == "GRANDMASTER" or tier == "CHALLENGER":
            response = get_league(tier, "")
            players = response['entries']
            playercount = 0
            for player in players:
                player_list.append(Player(player['summonerName'], player['summonerId'], "%s" % tier))
                playercount += 1
                if playercount >= players_per_league:
                    break
        else:
            for division in divisions:
                print("Request players from tier division %s." % division)
                response = get_league(tier, division)
                playercount = 0
                for player in response:
                    player_list.append(Player(player['summonerName'], player['summonerId'], "%s%s" % (tier, division)))
                    playercount += 1
                    if playercount >= players_per_league:
                        break

    # write list of players to file
    # file = open("players.txt", "w", encoding="utf-8")
    # for player in player_list:
    #     file.write("SummonerName: %s\tSummonerID: %s\n" % (player.name, player.id))

    return player_list


api_key = "RGAPI-e80a758a-421f-4f63-ab82-d4b9006896ca"
players_per_league = 1
output_file = "matches.csv"
redirect_stdout_to_log = True
log_file = "log.txt"


def prog():
    matches = dict()

    # collect a list of players using League API
    players = collect_players()

    print("---Done collecting players---")

    # fetch puuid for each player using Summoner API
    for player in players:
        response = get_summoner(player.id)
        player.puuid = response['puuid']

    print("---Done collecting puuids---")

    # fetch match list for each player's puuid using Match API
    for player in players:
        response = get_matches(player.puuid)
        match_id = response[0]  # take the first match only

        response = get_match(match_id)

        assert match_id == response['metadata']['matchId']

        m = Match(response)
        matches[match_id] = m

    print("---Done collecting matches---")

    for match in matches.values():
        match.process()

    print("---Done processing match data---")

    # write matches to file
    file = open(output_file, "w", encoding="utf-8")
    file.write("%s\n" % get_header())
    for match in matches.values():
        file.write("%s\n" % str(match))
    file.close()

    print("---Done writing match data to file---")
    print("Done.")


if __name__ == '__main__':
    if redirect_stdout_to_log:
        sys.stdout = open(log_file, "w", encoding="utf-8")

    prog()

    sys.stdout.close()
