import requests
import json
import time
import random


num_runs = 1
api_key = "RGAPI-659adc1e-559c-48ac-8be5-d8eca104719d"
players_per_league = 10
log_file = open("log.txt", "w", encoding="utf-8")
tiers = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND", "MASTER", "GRANDMASTER", "CHALLENGER"]
ranks = ["I", "II", "III", "IV"]
champions = []

# testing
# tiers = ["IRON"]
# ranks = ["II"]


class Player:
    name = ""
    id = ""
    puuid = ""
    from_rank = ""
    champion_name = ""
    champion_id = -1
    spell1id = -1
    spell2id = -1
    summoner_level = -1
    rank = ""
    wins = -1
    losses = -1
    veteran = -1
    hotStreak = -1

    def __init__(self, name, id):
        self.name = name.encode('utf-8')
        self.id = id

    def __str__(self):
        return "%s,%s,%s,%d,%d,%d,%d,%d,%d,%d" % \
               (self.name, self.rank, self.champion_name,
                self.spell1id, self.spell2id, self.summoner_level,
                self.wins, self.losses, self.veteran, self.hotStreak)


class Match:
    raw = ""
    winners = []
    losers = []
    match_id = ""
    rank_played_at = ""

    def __init__(self, raw, rank):
        self.raw = raw
        self.winners = []
        self.losers = []
        self.match_id = ""
        self.rank_played_at = rank

    def add_winner(self, winner_json):
        self.winners.append(winner_json)

    def add_lose(self, loser_json):
        self.losers.append(loser_json)

    def process(self):
        self.match_id = self.raw['metadata']['matchId']

        for play in self.raw['info']['participants']:
            p = Player(play['summonerName'], play['summonerId'])
            p.puuid = play['puuid']

            found_correct_queue = False
            # get player by puuid for further info
            if play['summonerId'] == "BOT":  # apparently Riot sometimes adds BOTs to the games. Thanks Riot.
                return False;

            response = get_league_by_encrypted_summonerid(play['summonerId'])

            if not response:
                bprint("Failed to get league data for summoner id %s." % play['summonerId'])
                return False

            for queue in response:
                if queue["queueType"] != "RANKED_SOLO_5x5":
                    continue  # skip over other queues
                found_correct_queue = True
                p.rank = rank_as_number(queue["tier"], queue["rank"])
                p.wins = queue["wins"]
                p.losses = queue["losses"]
                p.hotStreak = 1 if queue["hotStreak"] == "true" else 0
                p.veteran = 1 if queue["hotStreak"] == "true" else 0
                break

            if not found_correct_queue:
                bprint("Couldn't find queue.")
                return False

            p.champion_id = play['championId']
            p.champion_name = play['championName']

            if p.champion_name not in champions:
                champions.append(p.champion_name)

            p.spell1id = play['summoner1Id']
            p.spell2id = play['summoner2Id']
            p.summoner_level = play['summonerLevel']

            if play['win']:
                self.winners.append(p)
            else:
                self.losers.append(p)

        if len(self.winners) != 5 or len(self.losers) != 5:
            # bprint("Team was abnormally sized.")
            return False

        return True

    def __str__(self):
        s = "%s,%s" % (self.match_id, self.rank_played_at)
        first = []
        second = []

        # choose whether to put the winners or losers first
        winners_first = random.randint(0, 1) == 0
        if winners_first:
            first = self.winners
            second = self.losers
        else:
            first = self.losers
            second = self.winners

        def append_team(team):
            r = ""
            for play in team:
                r = "%s,%s" % (r, str(play))
            for champion in champions:
                champion_in_team = 0
                for play in team:
                    if play.champion_name == champion:
                        champion_in_team = 1
                        break
                r = "%s,%d" % (r, champion_in_team)
            # bprint("TEAM = " % r)
            return r

        s = "%s%s" % (s, append_team(first))
        s = "%s%s" % (s, append_team(second))

        # add which team won
        s = ("%s,1" if winners_first else "%s,2") % s
        return "%s" % s


rank_map = {
    "IRON IV": 0, "IRON III": 1, "IRON II": 2, "IRON I": 3,
    "BRONZE IV": 4, "BRONZE III": 5, "BRONZE II": 6, "BRONZE I": 7,
    "SILVER IV": 8, "SILVER III": 9, "SILVER II": 10, "SILVER I": 11,
    "GOLD IV": 12, "GOLD III": 13, "GOLD II": 14, "GOLD I": 15,
    "PLATINUM IV": 16, "PLATINUM III": 17, "PLATINUM II": 18, "PLATINUM I": 19,
    "DIAMOND IV": 20, "DIAMOND III": 21, "DIAMOND II": 22, "DIAMOND I": 23,
    "MASTER": 24, "GRANDMASTER": 25, "CHALLENGER": 26
}


def rank_as_number(tier, rank):
    if tier == "MASTER" or tier == "GRANDMASTER" or tier == "CHALLENGER":
        return rank_map[tier]
    return rank_map["%s %s" % (tier, rank)]


def make_header():
    header = "MATCH_ID,RANK_PLAYED_AT"

    for team in range(1, 3):
        for player in range(1, 6):
            player_header = "T%dP%dNAME,T%dP%dRANK,T%dP%dCHAMPION,T%dP%dSPELL1,T%dP%dSPELL2,T%dP%dSUMMONERLEVEL,T%dP%dWINS,T%dP%dLOSSES,T%dP%dVETERAN,T%dP%dHOTSTREAK" \
                            % (team, player, team, player, team, player, team, player, team, player, team, player, team, player, team, player, team, player, team, player)
            header += ",%s" % player_header
        champion_header = ""
        for champion in champions:
            champion_header += ",T%d%s" % (team, champion)
        header += "%s" % champion_header
    header += ",WINNINGTEAM"

    # bprint(header)

    return header


def request_until_success(request_url):
    success = False
    response = ""
    while not success:
        bprint("Sending request for %s." % request_url)
        response = requests.get(request_url)
        if response.status_code == 401 or response.status_code == 403:
            bprint("Response %d - May need to regenerate API key." % response.status_code)
            return False
        elif response.status_code == 429:
            sleeptime = int(response.headers["Retry-After"])
            bprint("Response %d - rate limit hit. Sleeping for %d and retrying later." % (response.status_code, sleeptime))
            time.sleep(sleeptime)
        elif response.status_code != 200:
            bprint("Response %d. Unexpected." % response.status_code)
            return False
        else:
            success = True
    assert response.status_code == 200  # sanity check
    return response


def get_match(match_id):
    bprint("Fetching match with match id %s." % match_id)
    url = "https://americas.api.riotgames.com/lol/match/v5/matches/%s?api_key=%s" % (match_id, api_key)
    response = request_until_success(url)
    if not response:
        return False
    return json.loads(response.text)


def get_matches(puuid):
    bprint("Fetching match data for player with puuid %s." % puuid)
    url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" \
          "%s/ids?start=0&count=20&api_key=%s" % (puuid, api_key)
    response = request_until_success(url)
    if not response:
        return False
    return json.loads(response.text)


def get_summoner(summoner_id):
    bprint("Fetching puuid for player with summoner id %s." % summoner_id)
    url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/%s?api_key=%s" % (summoner_id, api_key)
    response = request_until_success(url)
    if not response:
        return False
    return json.loads(response.text)


def get_league_by_encrypted_summonerid(summoner_id):
    bprint("Fetching league data for player with encrypted summoner id %s." % summoner_id)
    url = "https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/%s?api_key=%s" % (summoner_id, api_key)
    response = request_until_success(url)
    if not response:
        return False
    return json.loads(response.text)


def get_league_by_tier_rank(tier, rank):
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
              "RANKED_SOLO_5x5/%s/%s?page=1&api_key=%s" % (tier, rank, api_key)
    response = request_until_success(url)
    if not response:
        return False
    return json.loads(response.text)


def print_json(d):
    bprint(json.dumps(d, indent=4))


def format_json(d):
    return json.dumps(d, indent=4)


def collect_players():
    player_list = []

    # get a player from each league
    for tier in tiers:
        r = ""
        bprint("Requesting players from tier %s." % tier)
        if tier == "MASTER" or tier == "GRANDMASTER" or tier == "CHALLENGER":
            response = get_league_by_tier_rank(tier, "")
            if not response:
                bprint("Failed to get players from tier %s." % tier)
                continue
            players = response['entries']
            playercount = 0
            for player in players:
                p = Player(player['summonerName'], player['summonerId'])
                p.from_rank = tier
                player_list.append(p)
                playercount += 1
                if playercount >= players_per_league * 4:
                    break
        else:
            for rank in ranks:
                bprint("Request players from tier rank %s." % rank)
                response = get_league_by_tier_rank(tier, rank)
                if not response:
                    bprint("Failed to get players from tier %s rank %s." % (tier, rank))
                    continue
                playercount = 0
                for player in response:
                    p = Player(player['summonerName'], player['summonerId'])
                    p.from_rank = "%s %s" % (tier, rank)
                    player_list.append(p)
                    playercount += 1
                    if playercount >= players_per_league:
                        break

    # write list of players to file
    # file = open("players.txt", "w", encoding="utf-8")
    # for player in player_list:
    #     file.write("SummonerName: %s\tSummonerID: %s\n" % (player.name, player.id))

    return player_list


def bprint(s):
    log_file.write("%s\n" % s)
    print(s)


def collect(output_file):
    matches = dict()

    # collect a list of players using League API
    players = collect_players()

    bprint("---Done collecting players---")

    # fetch puuid for each player using Summoner API
    for player in players:
        response = get_summoner(player.id)
        if not response:
            bprint("Failed to get puuid from player %s." % player.id)
            continue
        player.puuid = response['puuid']

    bprint("---Done collecting puuids---")

    # fetch match list for each player's puuid using Match API
    for player in players:
        response = get_matches(player.puuid)
        if not response:
            bprint("Failed to get match list for player %s." % str(player.puuid))
            continue
        match_id = response[0]  # take the first match only

        response = get_match(match_id)
        if not response:
            bprint("Failed to get match data for match %s." % str(match_id))
            continue

        assert match_id == response['metadata']['matchId']

        m = Match(response, player.from_rank)
        matches[match_id] = m

    bprint("---Done collecting matches---")

    to_delete = []
    for key in matches.keys():
        match = matches[key]
        if not match.process():
            to_delete.append(key)
        else:
            bprint("Processed match %s." % match.match_id)

    bprint("List of champions in dataset: %s" % (str(champions)))

    bprint("Removing malformed matches...")
    num_malformed = 0
    for key in to_delete:
        # bprint("Removed %s." % key)
        num_malformed += 1
        matches.pop(key)
    bprint("Removed %d malformed matches." % num_malformed)

    bprint("---Done processing match data---")
    bprint("Writing match data to output file %s." % output_file)
    # write matches to file
    file = open(output_file, "w", encoding="utf-8")
    file.write("%s\n" % make_header())
    for match in matches.values():
        file.write("%s\n" % str(match))
    file.close()

    bprint("---Done writing match data to file---")
    bprint("-------------------------------------")


if __name__ == '__main__':
    for i in range(0, num_runs):
        try:
            collect("matches%d.csv" % i)
        except AssertionError:
            bprint("ASSERTION ERROR!")
    bprint("Done.")
    log_file.close()
