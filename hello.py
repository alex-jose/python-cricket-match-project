import yaml
import Match as m
import matplotlib.pyplot as plt
import numpy as np

currentTeam = ''
currentRuns = 0
teams = {}
fallofWickets = []
matchstats = {}

def oppTeam(team):
    for i in teams.keys():
        if i != team:
            return i
    print("ERROR: opposite team not found")
    return None

def getDelivery(data, name):
    global currentTeam
    global currentRuns
    global teams
    global fallofWickets
    global matchstats

    delivery = m.Delivery()
    delivery.name = name
    delivery.bowler = data['bowler']
    delivery.batsman = data['batsman']
    delivery.nonStriker = data['non_striker']
    delivery.batsmanRuns = data['runs']['batsman']
    delivery.extraRuns = data['runs']['extras']
    delivery.totalRuns = data['runs']['total']
    if 'non_boundary' in data['runs'].keys(): delivery.nonBoundary = data['runs']['non_boundary']
    if 'replacements' in data.keys():
        for k in data['replacements'].keys():
            for j in data['replacements'][k]:
                repl = m.Replacement()
                repl.kind = k
                repl.inPlayer = j['in']
                if 'out' in j.keys(): repl.outPlayer = j['out']
                repl.reason = j['reason']
                if 'role' in j.keys(): repl.role = j['role']
                if 'team' in j.keys(): repl.team = j['team']
                delivery.replacements.append(repl)
    if 'wicket' in data.keys():
        wicket = m.Wicket()
        wicket.kind = data['wicket']['kind']
        wicket.player_out = data['wicket']['player_out']
        if 'fielders' in data['wicket']: wicket.fielders =  data['wicket']['fielders']
        delivery.wicket = wicket
    if 'extras' in data.keys():
        delivery.extras = data['extras'];

    # stats
    if delivery.batsman not in teams[currentTeam].players.keys():
        teams[currentTeam].players[delivery.batsman] = m.Player(delivery.batsman)
    if delivery.nonStriker not in teams[currentTeam].players.keys():
        teams[currentTeam].players[delivery.nonStriker] = m.Player(delivery.nonStriker)
    if delivery.bowler not in teams[oppTeam(currentTeam)].players.keys():
        teams[oppTeam(currentTeam)].players[delivery.bowler] = m.Player(delivery.bowler)
    teams[currentTeam].players[delivery.batsman].batter = True
    teams[currentTeam].players[delivery.batsman].runs += delivery.batsmanRuns

    if delivery.batsmanRuns == 4: teams[currentTeam].players[delivery.batsman].fours += 1
    if delivery.batsmanRuns == 6: teams[currentTeam].players[delivery.batsman].sixes += 1

    if not (delivery.extras and len(delivery.extras) > 0):
        teams[currentTeam].players[delivery.batsman].ballsFaced += 1
        teams[oppTeam(currentTeam)].players[delivery.bowler].balls += 1

    if (delivery.wicket):
        fallofWickets.append((currentRuns, str(len(fallofWickets)), delivery.batsman, delivery.name, delivery.bowler))
        teams[oppTeam(currentTeam)].players[delivery.bowler].wickets += 1

    teams[oppTeam(currentTeam)].players[delivery.bowler].bowler = True
    teams[oppTeam(currentTeam)].players[delivery.bowler].runsGiven += data['runs']['total']
    currentRuns += delivery.totalRuns



    return delivery

def getInnings(data = {}, name = ''):
    global currentTeam
    innings = m.Innings()
    innings.deliveries = []
    innings.name = name
    innings.team = data['team']
    currentTeam = data['team']

    if 'absent_hurt' in data.keys(): innings.absentHurt = data['absent_hurt']
    if 'penalty_runs' in data.keys():
        d = data['penalty_runs']
        if 'pre' in d.keys(): innings.prePenaltyRuns = d['pre']
        if 'post' in d.keys(): innings.postPenaltyRuns = d['post']
    if 'declared' in data.keys(): innings.declared = data['decalred']
    for j in data['deliveries']:
        for i in j:
            delivery = getDelivery(j[i], i)
            innings.deliveries.append(delivery)
            # print("LOG:",innings.name,len(innings.deliveries))

    return innings

def getOutcome(data):
    outcome = m.Outcome()
    if ('by' in data.keys()):
        by = data['by']
        if ('innings' in by.keys()):
            outcome.by = 'innings'
            outcome.innings = by['innings']
        if ('runs' in by.keys()):
            outcome.by = 'runs'
            outcome.runs = by['runs']
        if ('wickets' in by.keys()):
            outcome.by = 'wickets'
            outcome.wickets = by['wickets']
    if ('method' in data.keys()): outcome.method = data['method']
    if ('bowlout' in data.keys()): outcome.bowlout = data['bowlout']
    if ('eliminator' in data.keys()): outcome.eliminator = data['eliminator']
    if ('result' in data.keys()): outcome.result = data['result']
    if ('winner' in data.keys()): outcome.winner = data['winner']
    return outcome

def getToss(data = {}):
    toss = m.Toss(data['winner'], data['decision'])
    return toss

def getMatch(data = {}):
    global teams
    match = m.Match(data['dates'], data['gender'], data['match_type'], getOutcome(data['outcome']), getToss(data['toss']), data['umpires'])

    if ('city' in data.keys()): match.city = data['city']
    if ('neutral_venue' in data.keys()): match.neutralVenue = data['neutral_venue']
    if ('competition' in data.keys()): match.competition = data['competition']
    if ('venue' in data.keys()): match.venue = data['venue']
    if ('player_of_match' in data.keys()): match.playerOfMatch = data['player_of_match']
    if ('supersubs' in data.keys()): match.supersubs = data['supersubs']
    if ('overs' in data.keys()): match.overs = data['overs']

    #todo
    if ('bowl_out' in data.keys()): match.bowlout = data['bowl_out']

    # teams
    for i in data['teams']:
        teams[i] = m.Team(i)

    return match

raw_data = open('567353.yaml').read()
yaml_dictionary = yaml.unsafe_load(raw_data)
data = yaml_dictionary

info = yaml_dictionary['info']

match = getMatch(info)

for j in data['innings']:
    for i in j:
        #print("LOG : ", j[i])
        currentRuns = 0
        fallofWickets = []
        inn = getInnings(j[i], i)
        match.addInnings(inn)
        teams[inn.team].fallOfWickets = fallofWickets
        teams[inn.team].runs = currentRuns
        teams[inn.team].wickets = len(fallofWickets)

match.teams = teams

# 1. match info
print("==========")
print("Match Info")
print("==========")
match.display()

# 2. batters
print("=======")
print("Batters")
print("=======")
for team in match.teams.keys():
    team = match.teams[team]
    print("    ", team.name)
    for player in team.players:
        player = team.players[player]
        if player.batter:
            print("    ", "    ", player.name)

# 3. bowlers
print("=======")
print("Bowlers")
print("=======")
for team in match.teams:
    team = match.teams[team]
    print("    ", team.name)
    for player in team.players:
        player = team.players[player]
        if player.bowler:
            print("    ", "    ", player.name)

# 4. Deliveries

print("==========")
print("Deliveries")
print("==========")

for innings in match.inningsList:
    print(innings.name, end = " : ")
    prefix = " " * len(innings.name) + "  "
    counter = 1
    for j in innings.deliveries:
        out = ""
        if j.extras:
            out = list(j.extras.keys())[0] + " "
        out += str(j.totalRuns)
        if j.wicket:
            out = "W"
        print(" (" + out + ")", end="")
        if counter % 30 == 0:
            print("\n", prefix, end = "")
        elif counter != len(innings.deliveries):
            print(",", end="")
        counter += 1
    if counter % 30 != 0: print()

# 5. del by over
print("==================")
print("Deliveries by Over")
print("==================")

for innings in match.inningsList:
    delbyover = {}
    print(innings.name)
    for delivery in innings.deliveries:
        if int(str(delivery.name).split(".")[0]) not in delbyover.keys():
            delbyover[int(str(delivery.name).split(".")[0])] = []
        delbyover[int(str(delivery.name).split(".")[0])].append(delivery)
    for i in sorted(delbyover.keys()):
        print(" ", i, "\t: ", end="")
        for j in delbyover[i]:
            out = ""
            if j.extras:
                out = list(j.extras.keys())[0] + " "
            out += str(j.totalRuns)
            if j.wicket:
                out = "W"
            print("("+ out + ")", end="")
        print("")

# 6. batter stats
print("==================")
print("Batting Statistics")
print("==================")
for i in match.teams:
    i = match.teams[i]
    print(i.name, " :- ")
    i.displayBatterStats()

# 7. match stats
print("==================")
print("Bowler Statistics")
print("==================")
for i in match.teams:
    i = match.teams[i]
    print(i.name, " :- ")
    i.displayBowlerStats()


def plot_overs(innings, color):
    delbyover = {}
    teamName = innings.team
    for delivery in innings.deliveries:
        if int(str(delivery.name).split(".")[0]) not in delbyover.keys():
            delbyover[int(str(delivery.name).split(".")[0])] = 0
        delbyover[int(str(delivery.name).split(".")[0])] += delivery.totalRuns
    label = delbyover.keys()
    values = delbyover.values()

    index = np.arange(len(label))
    plt.figure(num=teamName)
    plt.bar(index, values, color=color)
    plt.xlabel('Overs', fontsize=8)
    plt.ylabel('Runs', fontsize=8)
    plt.xticks(index, label, fontsize=8, rotation=30)
    plt.title(teamName + "-" + innings.name)
    plt.show()


plot_overs(match.inningsList[0], "red")
plot_overs(match.inningsList[1], "blue")


print("Thank You")