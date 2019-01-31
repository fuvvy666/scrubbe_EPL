import urllib2
from bs4 import BeautifulSoup
import json
import csv

# set the URL.
match_week = range(1,39)
url = "https://footballapi.pulselive.com:443/football/standings?compSeasons=79&altIds=true&detail=2&FOOTBALL_COMPETITION=1&gameweekNumbers=1-"

# set the header
header = {
	"Host":"footballapi.pulselive.com",
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
	#"Accept":" text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	#"Accept-Language":" zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
	"Referer":"https://www.premierleague.com/tables?co=1&se=79&ha=-1",
	"Origin":"https://www.premierleague.com"}

# open an csv.file
f = open('epl_4.csv', 'wb')
csv_writer = csv.writer(f)
column = ['match_week', 'starting_position', 'club', 'ave_goalsFor_home',
          'ave_goalsFor_away','ave_goalsAgainst_home', 'ave_goalsAgainst_away',
          'ave_points_home', 'ave_points_away']
csv_writer.writerow([x for x in column])

# variables in csv.file
match_week = ""
starting_position = ""
club = ""
ave_goalsFor_home = 0
ave_goalsFor_away = 0
ave_goalsAgainst_home = 0
ave_goalsAgainst_away = 0
ave_points_home = 0
ave_points_away = 0
ave_position_home = 0
ave_position_away = 0




def avePositions(data, k, club):
    sum = 0
    for i in range(k-5, k+1):
        sum = sum + data[str(i)][club]
    ave = float(sum) / 5
    return ave

def aveRound5(data, k, club):
    week_begin = k-5
    result = (float(data[str(k)][club])-float(data[str(week_begin)][club]))/5
    return result

home_goalsFor = {}
away_goalsFor = {}
home_goalsAgainst = {}
away_goalsAgainst = {}
#home_positions = {}
#away_positions = {}
home_points = {}
away_points = {}

# For every rounds.
for week in range(1,39):
    # the entire URL
    print(week)
    url_EPL = url + str(week)
    response = urllib2.Request(url_EPL, headers= header)
    page = urllib2.urlopen(response)
    # beautifulsoup
    soup = BeautifulSoup(page, features="lxml")
    table = soup.find('p')
    # class 'unicode' convert to class 'dic'
    t = table.text.encode('gbk')  # 'unicode' convert to 'str'
    t = json.loads(t)  # 'str' convert to 'dic'
    # all the info in 'dict'
    # keys in dict: 'form', 'away', 'team', 'overall', 'startingPosition', 'position',
    # 'home', 'annotations', 'ground'
    entries = t['tables'][0]['entries']
    home_goalsFor[str(week)] = {}
    away_goalsFor[str(week)] = {}
    home_goalsAgainst[str(week)] = {}
    away_goalsAgainst[str(week)] = {}
#    home_positions[str(week)] = {}
#    away_positions[str(week)] = {}
    home_points[str(week)] = {}
    away_points[str(week)] = {}
    for row in range(0,20):
        match_week = week
        if(week == 1):
            starting_position = entries[row]['position']
        else:
            starting_position = entries[row]['startingPosition']
        club = entries[row]['team']['name']
        home_goalsFor[str(week)][club] = entries[row]['home']['goalsFor']
        away_goalsFor[str(week)][club] = entries[row]['away']['goalsFor']
        home_goalsAgainst[str(week)][club] = entries[row]['home']['goalsAgainst']
        away_goalsAgainst[str(week)][club] = entries[row]['away']['goalsAgainst']
        home_points[str(week)][club] = entries[row]['home']['points']
        away_points[str(week)][club] = entries[row]['away']['points']
#        home_positions[str(week)][club] = entries[row]['home']['position']
        if(match_week<=5):
            continue
        else:
            ave_goalsFor_home = 0
            ave_goalsFor_away = 0
            ave_goalsAgainst_home = 0
            ave_goalsAgainst_away = 0
            k = week - 5
            ave_goalsFor_home = aveRound5(home_goalsFor, week, club)
            ave_goalsFor_away = aveRound5(away_goalsFor, week, club)
            ave_goalsAgainst_home = aveRound5(home_goalsAgainst, week, club)
            ave_goalsAgainst_away = aveRound5(away_goalsAgainst, week, club)
            ave_points_home = aveRound5(home_points, week, club)
            ave_points_away = aveRound5(away_points, week, club)
        csv_writer.writerow([x for x in [match_week, starting_position, club, ave_goalsFor_home, ave_goalsFor_away,
                                         ave_goalsAgainst_home, ave_goalsAgainst_away, ave_points_home, ave_points_away]])

f.close()

        
