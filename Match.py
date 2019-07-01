class Player:
    name = ''
    batter = False
    bowler = False
    runs = 0
    ballsFaced = 0
    fours = 0
    sixes = 0
    sr = 0

    balls = 0
    wickets = 0
    runsGiven = 0
    economy = 0

    def __init__(self, name):
        self.name = name

class Team:
    name = ''
    players = {}
    runs = 0
    wickets = 0
    fallOfWickets = []
    def __init__(self, name):
        self.name = name
        self.players = {}

    def displayBatterStats(self, prefix = ""):
        print(prefix + '    ', '    ', "name, runs, balls, fours, sixes, strikerate")
        for p in self.players.keys():
            p = self.players[p]
            if p.batter:
                strikerate = (p.runs * 100) / p.ballsFaced
                print(prefix + '    ', '    ', p.name, ",", p.runs, ",", p.ballsFaced, ",", p.fours, ",", p.sixes, ",", "%.2f" % (strikerate))

    def displayBowlerStats(self, prefix = ""):
        print(prefix + '    ', '    ', "name, overs, runs, wickets, economy")
        for p in self.players.keys():
            p = self.players[p]
            if p.bowler:
                economy = 6 * p.runsGiven / p.balls
                print(prefix + '    ', '    ', p.name, ",", str(p.balls//6) + '.' + str(p.balls % 6), ",", p.runsGiven, ",", p.wickets, ",", "%.2f" % (economy))

    def display(self, prefix = ''):
        print(prefix, 'TEAM: ' + self.name)
        print(prefix, '    ', self.runs, '/', self.wickets)
        print(prefix, '    ', 'Fall Of Wickets : ')
        for i in self.fallOfWickets:
            print(prefix, '    ', '    ', str(i[0]) + '/' + str(i[1]) + ' (' + i[2] + ', ' + str(i[3]) + ')')
        print(prefix, '    ', 'Batting : ')
        self.displayBatterStats(prefix)
        print(prefix, '    ', 'Bowling : ')
        self.displayBowlers()



class Replacement:
    kind = ''
    inPlayer = ''
    outPlayer = ''
    reason = ''
    role = ''
    team = ''


class Wicket:
    kind = ''
    player_out = ''
    fielders = []

    def __init__(self):
        self.fielders = []

class Delivery:
    name = ''
    batsman = ''
    nonStriker = ''
    bowler = ''
    batsmanRuns = 0
    extraRuns = 0
    nonBoundary = 0
    replacements = []
    wicket = None
    extras = {}
    totalRuns = 0

    def __init__(self):
        self.replacements = []



class Innings:
    name = ''
    team = ''
    deliveries = []
    absentHurt = []
    prePenaltyRuns = 0
    pstPenaltyRuns = 0
    declared = ''


    def __init__(self):
        self.deliveries = []
        self.absentHurt = []


class BowlOut:
    bowler = ''
    outcome = ''

    def __init__(self, bowler, outcome):
        self.bowler = bowler
        self.outcome = outcome

    def display(self, prefix=''):
        print(prefix, 'Bowler  : ', self.bowler)
        print(prefix, 'Outcome : ', self.outcome)


class Outcome:
    by = ''
    innings = 0
    wicket = 0
    runs = 0
    bowlout = ''
    eliminator = ''
    method = ''
    result = ''
    winner = ''

    def display(self, prefix=''):
        print(prefix, 'Outcome :-')
        if self.result != '':
            print(prefix, '    ', self.result)
            return
        if self.winner != '':
            print(prefix, '    ', self.winner, 'won')
            if self.eliminator:
                print(prefix, '    ', self.eliminator, 'won in eliminator')
            if self.bowlout:
                print(prefix, '    ', self.bowlout, 'won in bowl out')
            if self.by == 'innings':
                print(prefix, '    ', 'by ', self.innings, ' innings')
            elif self.by == 'runs':
                print(prefix, '    ', 'by ', self.runs, ' runs')
            elif self.by == 'wickets':
                print(prefix, '    ', 'by ', self.wickets, ' wickets')
            if self.method:
                print(prefix, '    ', 'using ', self.method, ' method')


class Toss:
    def __init__(self, winner, decision):
        self.winner = winner
        self.decision = decision

    def display(self, prefix = ''):
        print(prefix, 'Toss :-')
        print(prefix, '    ', self.winner, ' won toss and decided to ', self.decision)


class Match:
    bowlout = []  # optional
    city = ''  # opt
    competition = ''  # opt
    dates = []
    overs = 20
    playerOfMatch = ''
    supersubs = []
    teams = []
    toss = None
    umpires = []
    venue = ''  # opt
    neutralVenue = ''
    inningsList = []
    gender = ''
    matchType = ''
    outcome = ''

    def __init__(self, dates, gender, matchType, outcome, toss, umpires):
        self.dates = dates
        self.gender = gender
        self.matchType = matchType
        self.outcome = outcome
        self.toss = toss
        self.umpires = umpires

    def addInnings(self, innings):
        self.inningsList.append(innings)

    def addBowlout(self, bowler, outcome):
        self.bowlout.append(BowlOut(bowler, outcome))

    def display(self, prefix=''):
        print(prefix, 'Match Type          : ', self.matchType)
        print(prefix, 'Teams               :-')
        for t in self.teams:
            print(prefix, '    ', t)
        print(prefix, 'Gender              : ', self.gender)
        print(prefix, 'Innings             : ', len(self.inningsList))
        print(prefix, 'Dates               :-')
        for d in self.dates:
            print(prefix, '    ', d)
        print(prefix, 'Umpires         :-')
        for u in self.umpires:
            print(prefix, '    ', u)
        self.toss.display()
        self.outcome.display()

        # Optional
        if self.playerOfMatch:
            print(prefix, 'Player of Match : ', ', '.join(self.playerOfMatch))
        if self.overs:
            print(prefix, 'Overs           : ', self.overs)
        if self.competition:
            print(prefix, 'Competition     : ', self.competition)
        if self.neutralVenue:
            print(prefix, 'Neutral Venue   : ', self.neutralVenue)
        if self.city:
            print(prefix, 'City            : ', self.city)
        if self.venue:
            print(prefix, 'Venue           : ', self.venue)
        if len(self.bowlout) > 0:
            print(prefix, 'Bowlouts        :-')
            for b in self.bowlout:
                print(prefix, '    ', '*')
                b.display(prefix, '    ')

        print()