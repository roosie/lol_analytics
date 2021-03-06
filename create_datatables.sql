drop table participant;
drop table teams;
drop table matches;
drop table game;
drop table delta;

CREATE TABLE matches (
  platform varchar(60),
  gameId BIGINT PRIMARY KEY,
  champion INT,
  queue INT,
  season INT,
  timestampValue INT,
  role varchar(60),
  lane varchar(60)
);

CREATE TABLE game (
  platformId varchar(60),
  gameId BIGINT PRIMARY KEY,
  gameDuration  BIGINT,
  gameCreation  BIGINT,
  seasonId INT,
  mapId INT,
  queueId varchar(60),
  gameVersion varchar(60),
  gameMode varchar(60),
  gameType varchar(60),
  team1 varchar(60),
  team2 varchar(60)
);


CREATE TABLE teams (
   teamId varchar(60) PRIMARY KEY,
   gameId BIGINT,
   win VARCHAR(60),
   firstBlood VARCHAR(60),
   firstTower VARCHAR(60),
   firstInhibitor VARCHAR(60),
   firstBaron VARCHAR(60),
   firstDragon VARCHAR(60),
   firstRiftHerald VARCHAR(60),
   towerKills INT,
   inhibitorKills INT,
   baronKills INT,
   dragonKills INT,
   vilemawKills INT,
   riftHeraldKills INT,
   dominionVictoryScore INT,
   participantId1 VARCHAR(60),
   participantId2 VARCHAR(60),
   participantId3 VARCHAR(60),
   participantId4 VARCHAR(60),
   participantId5 VARCHAR(60),
   ban1 INT,
   ban2 INT,
   ban3 INT,
   ban4 INT,
   ban5 INT,
   firstpick INT
);

CREATE TABLE delta (
  id VARCHAR(60) PRIMARY KEY,
  ten FLOAT,
  twenty FLOAT,
  thirty FLOAT,
  fourty FLOAT,
  fifty FLOAT,
  sixty FLOAT
);


CREATE TABLE participant(
  participantId varchar(60) PRIMARY KEY,
  accountId VARCHAR(60),
  teamId varchar(60),
  championId INT,
  spellId1 INT,
  spellId2 INT,
  highestAchievedSeasonTier VARCHAR(60),
  win VARCHAR(60),
  item0 INT,
  item1 INT,
  item2 INT,
  item3 INT,
  item4 INT,
  item5 INT,
  item6 INT,
  kills INT,
  deaths INT,
  assists INT,
  largestKillingSpree INT,
  largestMultiKill INT,
  killingSprees INT,
  longestTimeSpentLiving INT,
  doubleKills INT,
  tripleKills INT,
  quadraKills INT,
  pentaKills INT,
  unrealKills INT,
  totalDamageDealt INT,
  magicDamageDealt INT,
  physicalDamageDealt INT,
  trueDamageDealt INT,
  largestCriticalStrike  INT,
  totalDamageDealtToChampions INT,
  magicDamageDealtToChampions INT,
  physicalDamageDealtToChampions INT,
  trueDamageDealtToChampions INT,
  totalHeal INT,
  totalUnitsHealed INT,
  damageSelfMitigated INT,
  damageDealtToObjectives INT,
  damageDealtToTurrets INT,
  visionScore INT,
  timeCCingOthers INT,
  totalDamageTaken INT,
  magicalDamageTaken INT,
  physicalDamageTaken INT,
  trueDamageTaken INT,
  goldEarned INT,
  goldSpent INT,
  turretKills INT,
  inhibitorKills INT,
  totalMinionsKilled INT,
  neutralMinionsKilled INT,
  neutralMinionsKilledTeamJungle INT,
  neutralMinionsKilledEnemyJungle INT,
  totalTimeCrowdControlDealt INT,
  champLevel INT,
  visionWardsBoughtInGame INT,
  sightWardsBoughtInGame INT,
  wardsPlaced INT,
  wardsKilled INT,
  firstBloodKill  VARCHAR(60),
  firstBloodAssist VARCHAR(60),
  firstTowerKill  VARCHAR(60),
  firstTowerAssist VARCHAR(60),
  firstinhibitorKill VARCHAR(60),
  firstinhibitorAssist VARCHAR(60),
  combatPlayerScore INT,
  objectivePlayerScore INT,
  totalPlayerScore INT,
  totalScoreRank  INT,
  playerScore0 INT,
  playerScore1 INT,
  playerScore2 INT,
  playerScore3 INT,
  playerScore4 INT,
  playerScore5 INT,
  playerScore6 INT,
  playerScore7 INT,
  playerScore8 INT,
  playerScore9 INT,
  perk0 INT,
  perk0Var1 INT,
  perk0Var2 INT,
  perk0Var3 INT,
  perk1 INT,
  perk1Var1 INT,
  perk1Var2 INT,
  perk1Var3 INT,
  perk2 INT,
  perk2Var1 INT,
  perk2Var2 INT,
  perk2Var3 INT,
  perk3 INT,
  perk3Var1 INT,
  perk3Var2 INT,
  perk3Var3 INT,
  perk4 INT,
  perk4Var1 INT,
  perk4Var2 INT,
  perk4Var3 INT,
  perk5 INT,
  perk5Var1 INT,
  perk5Var2 INT,
  perk5Var3 INT,
  perkPrimaryStyle INT,
  perkSubStyle INT,
  statPerk0 INT,
  statPerk1 INT,
  statPerk2 INT,
  creepsPerMinDeltasId VARCHAR(60),
  xpPerMinDeltasId VARCHAR(60),
  goldPerMinDeltasId VARCHAR(60),
  damageTakenPerMinDeltasId VARCHAR(60),
  role VARCHAR(60),
  lane VARCHAR(60)
);
