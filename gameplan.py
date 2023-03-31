from colored import fg, bg, attr


class Team:
    def __init__(self, name, abbr, code, rank=0):
        super().__init__()
        self.name = name
        self.abbr = abbr
        self.rank = rank
        self.fg_color = code
        self.matches = []
        self.weekbg = {'Mon': 229,
                       'Tue': 230,
                       'Wed': 157,
                       'Thu': 193,
                       'Fri': 195,
                       'Sat': 223,
                       'Sun': 225}

    def add_match(self, match):
        # print('Adding match %s to Team %s' % (match.id, self.name))
        self.matches.append(match)

    def list_matches(self):
        sorted_list = sorted(self.matches, key=lambda x: x.id)
        for match in sorted_list:
            print(match)

    def heat_map(self, start, max_matches):
        matches = {match.id:match for match in self.matches}
        res = []
        for i in range(1, max_matches+1):
            if i in matches:
                bg_color = self.weekbg[matches[i].day]
                res.append('%s%s*%s' % (fg(self.fg_color), bg(bg_color), attr(0)))
            else:
                res.append('%s=%s' % (fg(self.fg_color), attr(0)))

        # Focus with in the range
        res = res[start-1:]

        print("%s%s%s\t\t%s" % (fg(self.fg_color), self.abbr, attr(0), ''.join(res)))


    def heat_map_wo_bg(self, start, max_matches):
        matches = {match.id:match for match in self.matches}
        res = ['%s%s%s' % (fg(255 if i in matches else self.fg_color),
                           '*' if i in matches else '=',
                           attr(0))
               for i in range(1, max_matches+1)]

        # Focus with in the range
        res = res[start-1:]
        return res


class Venue:
    def __init__(self, name:str, sym:str):
        self.name = name
        self.sym = sym
        self.matches = []

    def add_match(self, match:any):
        # print('Adding match %s to the Venue %s' % (match.id, self.name))
        self.matches.append(match)

    def list_matches(self):
        sorted_list = sorted(self.matches, key=lambda x: x.id)
        for match in sorted_list:
            print(match)


class Match:
    def __init__(self, match_day:int, match_id:int, teamA:Team, teamB:Team, venue:Venue, date:str, day:str, time:str):
        super().__init__()
        self.day = match_day
        self.id = match_id
        self.teams = [teamA, teamB]
        self.venue = venue
        self.date = date
        self.day = day
        self.time = time
        self.update()

    def update(self):
        for team in self.teams:
            team.add_match(self)
        self.venue.add_match(self)

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
        # print(self.teams)

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
                match_day, match_id, day, date, time, teamA, teamB, venue = line.strip().split('\t')
                self.matches.append(Match(int(match_day),
                                          int(match_id),
                                          self.teams[teamA],
                                          self.teams[teamB],
                                          self.venues[venue],
                                          date,
                                          day,
                                          time))

    def list_matches(self):
        sorted_list = sorted(self.matches, key=lambda x: x.id)
        for match in sorted_list:
            print(match)

    def day_map(self, start):
        cmap = {
                'Mon': '%sM%s'%(fg(229), attr(0)),
                'Tue': '%sT%s'%(fg(230), attr(0)),
                'Wed': '%sW%s'%(fg(157), attr(0)),
                'Thu': '%st%s'%(fg(193), attr(0)),
                'Fri': '%sF%s'%(fg(195), attr(0)),
                'Sat': '%sS%s'%(fg(223), attr(0)),
                'Sun': '%s$%s'%(fg(225), attr(0))
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

    def heat_maps(self, start=1, max_matches=80):
        teams = sorted(self.teams.items(), key=lambda x: x[1].rank)
        self.day_map(start)
        map_list = []
        for name, team in teams:
            res = team.heat_map_wo_bg(start, max_matches)
            density = self.match_density(res)
            map_list.append((density[0] , "%s%s%s\t\t%s" % (fg(team.fg_color), team.abbr, attr(0), ''.join(res))))

        print("\n".join([y for _, y in sorted(map_list, key=lambda t: -t[0])]))
        self.venue_map(start)

        # print("\n".join([str(x) for x, _ in sorted(map_list, key=lambda t: -t[0])]))

    def match_density(self, fixture):
        last_match = None
        count = 0
        max_offset = 2
        density = []
        for idx, data in enumerate(fixture[::-1]):
            update = 0
            if '*' in data:
                count += 1
                update = count
                last_match = idx
            elif last_match:
                if (idx - last_match) > max_offset:
                    count = 0
                update = max(0, count - 0.5)
            density.append(update)

        return density[::-1]


if "__main__"  == __name__:
   gameplan = Gameplan("teams.tsv", "venues.tsv", "fixtures.tsv")
   gameplan.heat_maps()