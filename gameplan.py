from colored import fg, bg, attr


class Team:
    def __init__(self, name, abbr, code, rank=0):
        super().__init__()
        self.name = name
        self.abbr = abbr
        self.rank = rank
        self.fg_color = code
        self.matches = []

    def add_match(self, match):
        print('Adding match %s to Team %s' % (match.id, self.name))
        self.matches.append(match)

    def list_matches(self):
        sorted_list = sorted(self.matches, key=lambda x: x.id)
        for match in sorted_list:
            print(match)

    def heat_map(self, start, max_matches):
        matches = set([match.id for match in self.matches])
        res = ['*' if i in matches else '%s=%s' % (fg(self.fg_color), attr(0)) for i in range(1, max_matches+1)][start-1:]
        print("%s%s%s\t\t%s" % (fg(self.fg_color), self.abbr, attr(0), ''.join(res)))
            

class Venue:
    def __init__(self, name:str, sym:str):
        self.name = name
        self.sym = sym
    
    def add_match(self, match:any):
        print('Adding match %s to the Venue %s' % (match.id, self.name))

    def list_matches(self):
        sorted_list = sorted(self.matches, key=lambda x: x.id)
        for match in sorted_list:
            print(match)


class Match:
    def __init__(self, match_id:int, teamA:Team, teamB:Team, venue:Venue, date:str, day:str):
        super().__init__()
        self.id = match_id
        self.teams = [teamA, teamB]
        self.venue = venue
        self.date = date 
        self.day = day
        self.update_teams()

    def update_teams(self):
        for team in self.teams:
            team.add_match(self)

    def __str__(self):
        return "\nMatch %s - %s\n%s\t\tvs\t\t%s\n%s" % (self.id, self.date, self.teams[0].name, self.teams[1].name, self.venue.name)


class Gameplan:
    def __init__(self, teams_file:str, venue_file:str, fixtures:str):
        super().__init__()
        self.load_teams(teams_file)
        self.load_venues(venue_file)
        self.load_matches(fixtures)
        
    def load_teams(self, teams_file):
        self.teams = dict()
        with open(teams_file, 'r') as tf:
            lines = tf.readlines()
            for line in lines:
                name, abbr, code = line.strip().split('\t')
                self.teams[abbr] = Team(name, abbr, code)

    def load_venues(self, venue_file):
        self.venues = dict()
        with open(venue_file, 'r') as tf:
            lines = tf.readlines()
            for line in lines:
                name, sym = line.strip().split('\t')
                self.venues[name] = Venue(name, sym)
    
    def load_matches(self, fixtures):
        self.matches = list()
        with open(fixtures, 'r') as ff:
            lines = ff.readlines()
            for line in lines:
                match_id, day, date, venue, teamA, teamB = line.strip().split('\t')
                self.matches.append(Match(int(match_id),
                                          self.teams[teamA],
                                          self.teams[teamB],
                                          self.venues[venue],
                                          date,
                                          day))

    def list_matches(self):
        sorted_list = sorted(self.matches, key=lambda x: x.id)
        for match in sorted_list:
            print(match)


    def day_map(self, start):
        cmap = {
                'MON': '%sM%s'%(fg(154), attr(0)),
                'TUE': '%sT%s'%(fg(9), attr(0)),
                'WED': '%sW%s'%(fg(46), attr(0)),
                'THU': '%st%s'%(fg(154), attr(0)),
                'FRI': '%sF%s'%(fg(9), attr(0)),
                'SAT': '%sS%s'%(fg(46), attr(0)),
                'SUN': '%s$%s'%(fg(9), attr(0))
                }
        sorted_list = sorted(self.matches, key=lambda x: x.id)
        venue = [cmap[x.day] for x in sorted_list][start-1:]
        print("\t\t%s" % (''.join(venue)))

    def venue_map(self, start):
        # cmap = {'A': '%s~%s'%(fg(154), attr(0)),
        #         'D': '%s^%s'%(fg(9), attr(0)),
        #         'S': '%s$%s'%(fg(46), attr(0))}
        sorted_list = sorted(self.matches, key=lambda x: x.id)
        # venue = [cmap[x.venue[0]] for x in sorted_list][start-1:]
        venue = [x.venue.sym for x in sorted_list][start-1:]
        print("\t\t%s" % (''.join(venue)))
        

    def heat_maps(self, start=1, max_matches=60):
        teams = sorted(self.teams.items(), key=lambda x: x[1].rank)
        self.day_map(start)
        for name, team in teams:
            team.heat_map(start, max_matches)
        self.venue_map(start)


if "__main__"  == __name__:
   gameplan = Gameplan("teams.tsv", "venues.tsv", "fixtures.tsv")
   gameplan.heat_maps()