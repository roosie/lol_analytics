import requests
import os
import json
import psycopg2
import uuid
import time
import sys

def get_summoner(name, region):
    API_KEY = os.environ['RIOT_API_KEY']
    header = {
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": API_KEY,
        "Accept-Language": "en-US,en;q=0.9"
    }
    r = requests.get(url='https://' + region + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name,
                     headers=header)
    r_summoner = json.loads(str(r.text))
    return r_summoner


def get_matchlist(account_id, region):
    API_KEY = os.environ['RIOT_API_KEY']
    header = {
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": API_KEY,
        "Accept-Language": "en-US,en;q=0.9"
    }
    r = requests.get(url='https://' + region + '.api.riotgames.com/lol/match/v4/matchlists/by-account/' + account_id,
                     headers=header)
    r_matchlist = json.loads(str(r.text))
    return r_matchlist

def get_match(match_id, region):
    API_KEY = os.environ['RIOT_API_KEY']
    header = {
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": API_KEY,
        "Accept-Language": "en-US,en;q=0.9"
    }
    r = requests.get(url='https://' + region + '.api.riotgames.com/lol/match/v4/matches/' + str(match_id),
                     headers=header)
    r_match = json.loads(str(r.text))
    return r_match

def delta_query_constructor(id, name, participant):
    fields = "(id, ten, twenty,thirty, fourty)"
    inputs = (id, participant.get("timeline", {}).get(name, {}).get("0-10", 0), participant.get("timeline", {}).get(name, {}).get("10-20", 0), participant.get("timeline", {}).get(name, {}).get("20-30", 0), participant.get("timeline", {}).get(name, {}).get("30-end", 0))
    return ("INSERT INTO delta" + fields + "values (%s,%s,%s,%s, %s);", inputs)

def participant_query_constructor(participant, participantIdentities, participantId):
    creepsPerMinDeltasId_uuid = str(uuid.uuid4())
    xpPerMinDeltasId_uuid = str(uuid.uuid4())
    goldPerMinDeltasId_uuid = str(uuid.uuid4())
    damageTakenPerMinDeltasId_uuid = str(uuid.uuid4())
    fields = "(participantId,accountId,teamId,championId,spellId1,spellId2,highestAchievedSeasonTier,win,item0,item1,item2,item3,item4,item5,item6,kills,deaths,assists,largestKillingSpree,largestMultiKill,killingSprees,longestTimeSpentLiving,doubleKills,tripleKills,quadraKills,pentaKills,unrealKills,totalDamageDealt,magicDamageDealt,physicalDamageDealt,trueDamageDealt,largestCriticalStrike,totalDamageDealtToChampions,magicDamageDealtToChampions,physicalDamageDealtToChampions,trueDamageDealtToChampions,totalHeal,totalUnitsHealed,damageSelfMitigated,damageDealtToObjectives,damageDealtToTurrets,visionScore,timeCCingOthers,totalDamageTaken,magicalDamageTaken,physicalDamageTaken,trueDamageTaken,goldEarned,goldSpent,turretKills,inhibitorKills,totalMinionsKilled,neutralMinionsKilled,neutralMinionsKilledTeamJungle,neutralMinionsKilledEnemyJungle,totalTimeCrowdControlDealt,champLevel,visionWardsBoughtInGame,sightWardsBoughtInGame,wardsPlaced,wardsKilled,firstBloodKill,firstBloodAssist,firstTowerKill,firstTowerAssist,firstInhibitorKill,firstInhibitorAssist,combatPlayerScore,objectivePlayerScore,totalPlayerScore,totalScoreRank,playerScore0,playerScore1,playerScore2,playerScore3,playerScore4,playerScore5,playerScore6,playerScore7,playerScore8,playerScore9,perk0,perk0Var1,perk0Var2,perk0Var3,perk1,perk1Var1,perk1Var2,perk1Var3,perk2,perk2Var1,perk2Var2,perk2Var3,perk3,perk3Var1,perk3Var2,perk3Var3,perk4,perk4Var1,perk4Var2,perk4Var3,perk5,perk5Var1,perk5Var2,perk5Var3,perkPrimaryStyle,perkSubStyle,statPerk0,statPerk1,statPerk2,creepsPerMinDeltasId,xpPerMinDeltasId,goldPerMinDeltasId,damageTakenPerMinDeltasId,role,lane)"
    inputs = (
        participantId, participantIdentities.get("player", "None").get("accountId", "None"),
        participant.get("teamId", "None"), participant.get("championId", "None"),
        participant.get("spell1Id", "None"), participant.get("spell2Id", "None"),
        participant.get("highestAchievedSeasonTier", "None"),
        participant.get("stats", "None").get("win", "None"), participant.get("stats", "None").get("item0", "None"),
        participant.get("stats", "None").get("item1", "None"),
        participant.get("stats", "None").get("item2", "None"), participant.get("stats", "None").get("item3", "None"),
        participant.get("stats", "None").get("item4", "None"),
        participant.get("stats", "None").get("item5", "None"), participant.get("stats", "None").get("item6", "None"),
        participant.get("stats", "None").get("kills", "None"),
        participant.get("stats", "None").get("deaths", "None"), participant.get("stats", "None").get("assists", "None"),
        participant.get("stats", "None").get("largestKillingSpree", "None"),
        participant.get("stats", "None").get("largestMultiKill", "None"),
        participant.get("stats", "None").get("killingSprees", "None"),
        participant.get("stats", "None").get("longestTimeSpentLiving", "None"),
        participant.get("stats", "None").get("doubleKills", "None"),
        participant.get("stats", "None").get("tripleKills", "None"),
        participant.get("stats", "None").get("quadraKills", "None"), participant.get("stats", "None").get("pentaKills", "None"),
        participant.get("stats", "None").get("unrealKills", "None"),
        participant.get("stats", "None").get("totalDamageDealt", "None"),
        participant.get("stats", "None").get("magicDamageDealt", "None"),
        participant.get("stats", "None").get("physicalDamageDealt", "None"),
        participant.get("stats", "None").get("trueDamageDealt", "None"),
        participant.get("stats", "None").get("largestCriticalStrike", "None"),
        participant.get("stats", "None").get("totalDamageDealtToChampions", "None"),
        participant.get("stats", "None").get("magicDamageDealtToChampions", "None"),
        participant.get("stats", "None").get("physicalDamageDealtToChampions", "None"),
        participant.get("stats", "None").get("trueDamageDealtToChampions", "None"),
        participant.get("stats", "None").get("totalHeal", "None"),
        participant.get("stats", "None").get("totalUnitsHealed", "None"),
        participant.get("stats", "None").get("damageSelfMitigated", "None"),
        participant.get("stats", "None").get("damageDealtToObjectives", "None"),
        participant.get("stats", "None").get("damageDealtToTurrets", "None"),
        participant.get("stats", "None").get("visionScore", "None"),
        participant.get("stats", "None").get("timeCCingOthers", "None"),
        participant.get("stats", "None").get("totalDamageTaken", "None"),
        participant.get("stats", "None").get("magicalDamageTaken", "None"),
        participant.get("stats", "None").get("physicalDamageTaken", "None"),
        participant.get("stats", "None").get("trueDamageTaken", "None"),
        participant.get("stats", "None").get("goldEarned", "None"), participant.get("stats", "None").get("goldSpent", "None"),
        participant.get("stats", "None").get("turretKills", "None"),
        participant.get("stats", "None").get("inhibitorKills", "None"),
        participant.get("stats", "None").get("totalMinionsKilled", "None"),
        participant.get("stats", "None").get("neutralMinionsKilled", "None"),
        participant.get("stats", "None").get("neutralMinionsKilledTeamJungle", "None"),
        participant.get("stats", "None").get("neutralMinionsKilledEnemyJungle", "None"),
        participant.get("stats", "None").get("totalTimeCrowdControlDealt", "None"),
        participant.get("stats", "None").get("champLevel", "None"),
        participant.get("stats", "None").get("visionWardsBoughtInGame", "None"),
        participant.get("stats", "None").get("sightWardsBoughtInGame", "None"),
        participant.get("stats", "None").get("wardsPlaced", "None"),
        participant.get("stats", "None").get("wardsKilled", "None"),
        participant.get("stats", "None").get("firstBloodKill", "None"),
        participant.get("stats", "None").get("firstBloodAssist", "None"),
        participant.get("stats", "None").get("firstTowerKill", "None"),
        participant.get("stats", "None").get("firstTowerAssist", "None"),
        participant.get("stats", "None").get("firstInhibitorKill", "None"),
        participant.get("stats", "None").get("firstInhibitorAssist", "None"),
        participant.get("stats", "None").get("combatPlayerScore", "None"),
        participant.get("stats", "None").get("objectivePlayerScore", "None"),
        participant.get("stats", "None").get("totalPlayerScore", "None"),
        participant.get("stats", "None").get("totalScoreRank", "None"),
        participant.get("stats", "None").get("playerScore0", "None"),
        participant.get("stats", "None").get("playerScore1", "None"),
        participant.get("stats", "None").get("playerScore2", "None"),
        participant.get("stats", "None").get("playerScore3", "None"),
        participant.get("stats", "None").get("playerScore4", "None"),
        participant.get("stats", "None").get("playerScore5", "None"),
        participant.get("stats", "None").get("playerScore6", "None"),
        participant.get("stats", "None").get("playerScore7", "None"),
        participant.get("stats", "None").get("playerScore8", "None"),
        participant.get("stats", "None").get("playerScore9", "None"), participant.get("stats", "None").get("perk0", "None"),
        participant.get("stats", "None").get("perk0Var1", "None"), participant.get("stats", "None").get("perk0Var2", "None"),
        participant.get("stats", "None").get("perk0Var3", "None"),
        participant.get("stats", "None").get("perk1", "None"), participant.get("stats", "None").get("perk1Var1", "None"),
        participant.get("stats", "None").get("perk1Var2", "None"),
        participant.get("stats", "None").get("perk1Var3", "None"), participant.get("stats", "None").get("perk2", "None"),
        participant.get("stats", "None").get("perk2Var1", "None"),
        participant.get("stats", "None").get("perk2Var2", "None"), participant.get("stats", "None").get("perk2Var3", "None"),
        participant.get("stats", "None").get("perk3", "None"),
        participant.get("stats", "None").get("perk3Var1", "None"), participant.get("stats", "None").get("perk3Var2", "None"),
        participant.get("stats", "None").get("perk3Var3", "None"),
        participant.get("stats", "None").get("perk4", "None"), participant.get("stats", "None").get("perk4Var1", "None"),
        participant.get("stats", "None").get("perk4Var2", "None"),
        participant.get("stats", "None").get("perk4Var3", "None"), participant.get("stats", "None").get("perk5", "None"),
        participant.get("stats", "None").get("perk5Var1", "None"),
        participant.get("stats", "None").get("perk5Var2", "None"), participant.get("stats", "None").get("perk5Var3", "None"),
        participant.get("stats", "None").get("perkPrimaryStyle", "None"),
        participant.get("stats", "None").get("perkSubStyle", "None"), participant.get("stats", "None").get("statPerk0", "None"),
        participant.get("stats", "None").get("statPerk1", "None"),
        participant.get("stats", "None").get("statPerk2", "None"), creepsPerMinDeltasId_uuid, xpPerMinDeltasId_uuid,
        goldPerMinDeltasId_uuid,
        damageTakenPerMinDeltasId_uuid, participant.get("timeline", "None").get("role", "None"),
        participant.get("timeline", "None").get("lane", "None"))

    r_participant = ("INSERT INTO participant" + fields + "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", inputs)
    creepsPerMinDeltas = delta_query_constructor(creepsPerMinDeltasId_uuid, "creepsPerMinDeltas", participant)
    xpPerMinDeltas = delta_query_constructor(xpPerMinDeltasId_uuid, "xpPerMinDeltas", participant)
    goldPerMinDeltas = delta_query_constructor(goldPerMinDeltasId_uuid, "goldPerMinDeltas", participant)
    damageTakenPerMinDeltas = delta_query_constructor(damageTakenPerMinDeltasId_uuid, "damageTakenPerMinDeltas", participant)

    return [r_participant, creepsPerMinDeltas, xpPerMinDeltas, goldPerMinDeltas, damageTakenPerMinDeltas]

def teams_query_constructor(team, teamId, matchId, participants, participantIdentities):
    executelist = []
    firstPick = 1 if team["bans"][0]["pickTurn"] == 1 else 0
    participantId1 = str(uuid.uuid4())
    participantId2 = str(uuid.uuid4())
    participantId3 = str(uuid.uuid4())
    participantId4 = str(uuid.uuid4())
    participantId5 = str(uuid.uuid4())
    fields = "(teamId, gameId, win, firstBlood, firstTower, firstInhibitor, firstBaron, firstDragon, firstRiftHerald, towerKills, inhibitorKills, baronKills, dragonKills, vilemawKills, riftHeraldKills, dominionVictoryScore, participantId1, participantId2, participantId3, participantId4, participantId5, ban1, ban2, ban3, ban4, ban5, firstpick)"
    inputs = (teamId, matchId, team.get("win", "None"), team.get("firstBlood", "None"), team.get("firstTower", "None"),
              team.get("firstInhibitor", "None"), team.get("firstBaron", "None"), team.get("firstDragon", "None"),
              team.get("firstRiftHerald", "None"), team.get("towerKills", "None"), team.get("inhibitorKills", "None"),
              team.get("baronKills", "None"), team.get("dragonKills", "None"), team.get("vilemawKills", "None"),
              team.get("riftHeraldKills", "None"), team.get("dominionVictoryScore", "None"), participantId1, participantId2,
              participantId3, participantId4, participantId5,
              team.get("bans", "None")[0].get("championId", "None"),
              team.get("bans", "None")[1].get("championId", "None"),
              team.get("bans", "None")[2].get("championId", "None"),
              team.get("bans", "None")[3].get("championId", "None"),
              team.get("bans", "None")[4].get("championId", "None"), firstPick)
    executelist.append(("INSERT INTO teams" + fields + "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", inputs))
    one = 0 if team["teamId"] == 100 else 5
    two = 1 if team["teamId"] == 100 else 6
    three = 2 if team["teamId"] == 100 else 7
    four = 3 if team["teamId"] == 100 else 8
    five = 4 if team["teamId"] == 100 else 9
    executelist += participant_query_constructor(participants[one], participantIdentities[one], participantId1)
    executelist += participant_query_constructor(participants[two], participantIdentities[two],
                                                 participantId2)
    executelist += participant_query_constructor(participants[three], participantIdentities[three],
                                                 participantId3)
    executelist += participant_query_constructor(participants[four], participantIdentities[four],
                                                 participantId4)
    executelist += participant_query_constructor(participants[five], participantIdentities[five],
                                                 participantId5)
    return executelist

def game_query_constructor(game):
    executelist = []
    team_id_1 = str(uuid.uuid4())
    team_id_2 = str(uuid.uuid4())
    fields = "(platformId, gameId, gameDuration, gameCreation, seasonId, mapId, queueId, gameVersion, gameMode, gameType, team1, team2)"
    inputs = (game.get("platformId", "None"), game.get("gameId", "None"), game.get("gameDuration", "None"), game.get("gameCreation", "None"), game.get("seasonId", "None"), game.get("mapId", "None"), game.get("queueId", "None"), game.get("gameVersion", "None"), game.get("gameMode", "None"), game.get("gameType", "None"), team_id_1, team_id_2)
    executelist.append(("INSERT INTO game" + fields + "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", inputs))
    executelist += teams_query_constructor(game["teams"][0], team_id_1, game["gameId"], game["participants"], game["participantIdentities"])
    executelist += teams_query_constructor(game["teams"][1], team_id_2, game["gameId"], game["participants"], game["participantIdentities"])
    return executelist

def insert_match(match):
    host = os.environ['HOST']
    user = os.environ['USER']
    password = os.environ['PASSWORD']
    with psycopg2.connect(host=host, user=user, password=password) as conn:
        curr = conn.cursor()
        queries = game_query_constructor(match)
        try:
            for query in queries:
                curr.execute(query[0], query[1])
            conn.commit()
            return "success"
        except Exception as e:
            print("failed to insert", query[0], query[1], str(e))
            return "fail"

def get_related_matches(name, region, count):
    for i in range(count):
        summoner = get_summoner(name, region)
        print(summoner)
        matchlist = get_matchlist(summoner["accountId"], region)
        print(matchlist)
        matches = matchlist['matches'][:10]
        match = ""
        for m in matches:
            time.sleep(30)
            match = get_match(m["gameId"], 'na1')
            if match['gameType'] == 'MATCHED_GAME' and match['gameMode'] == 'CLASSIC':
                print(match)
                insert_match(match)
        name = match['participantIdentities'][5]['player']['summonerName'] if match['participantIdentities'][5]['player']['summonerName'] != name else match['participantIdentities'][1]['player']['summonerName']

def get_matches(summoner, region, count):
    #stop from running going forever, just in case
    limiter = 100
    player_stack = []
    visited = set()
    player_stack.append(summoner)
    while count > 0:
        player = player_stack.pop()
        summoner = get_summoner(player, region)
        matchlist = get_matchlist(summoner["accountId"], region)
        #TODO find a better way of determining current patch time, currently compares to release time of 9.18\
        matches = list(filter(lambda x: (x["timestamp"] > 1568205138000), matchlist['matches']))
        match = ""
        for m in matches:
            time.sleep(10)
            match = get_match(m["gameId"], 'na1')
            if match['gameType'] == 'MATCHED_GAME' and match['gameMode'] == 'CLASSIC':
                insert_match(match)
                count -= 1
                for part in match['participantIdentities']:
                    if part['player']['summonerName'] not in visited:
                        player_stack.append(part['player']['summonerName'])
        print(len(matches))
        match = ""
        limiter -= 1
        if limiter < 0:
            break
def get_playrate_and_winrate(id):
    host = os.environ['HOST']
    user = os.environ['USER']
    password = os.environ['PASSWORD']
    with psycopg2.connect(host=host, user=user, password=password) as conn:
        curr = conn.cursor()
        curr.execute("select win.winCount, lose.loseCount from (select count(*) as winCount from participant where win = 'true' and championId = %s) as win, (select count(*) as loseCount from participant where win = 'false' and championId = %s) as lose;", (id, id))
        conn.commit()
        x = curr.fetchone()
    return (id,x[0],x[1])

def get_playrate_and_winrate_items(id):
    host = os.environ['HOST']
    user = os.environ['USER']
    password = os.environ['PASSWORD']
    with psycopg2.connect(host=host, user=user, password=password) as conn:
        curr = conn.cursor()
        curr.execute("select win.winCount, lose.loseCount from (select count(*) as winCount from participant where win = 'true' and (item0 = %s or item1 = %s or item2 = %s or item3 = %s or item4 = %s or item5 = %s or item6 = %s)) as win, (select count(*) as loseCount from participant where win = 'false' and (item0 = %s or item1 = %s or item2 = %s or item3 = %s or item4 = %s or item5 = %s or item6 = %s)) as lose;", (id, id))
        conn.commit()
        x = curr.fetchone()
    return (id,x[0],x[1])

#get_related_matches(sys.argv[1], sys.argv[2], sys.argv[3])
