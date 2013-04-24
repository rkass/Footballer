import settings
from django.core.management import setup_environ
setup_environ(settings)
from stats.models import Game
import sys
import csv
  
def changeDate(d):
  return d[6:] + "-" + d[0:2] + "-" + d[3:5]

def timeToSeconds(t):
  return float(t[0:2]) * 60 + float(t[3:])

notduplicated = []
teamteam = []
dups, games, ignored = 0, 0, 0
f = open(sys.argv[1], 'r')
stats = csv.reader(f)
flag = True
for row in stats:
  if flag:
    flag = False
    continue
  g = Game(date = changeDate(row[0]))
  if sys.argv[2] != 'l':
    if row[30] == 'H':
      g.teamH = row[1]
      g.scoreH = row[2]
      g.firstDownH = row[3]
      g.thirdDownPctH = float(row[4][0:-1]) / 100
      g.rushAttH = row[5]
      g.rushYdsH = row[6]
      g.passAttH = row[7]
      g.passCompH = row[8]
      g.passYdsH = row[9]
      g.passIntH = row[10]
      g.fumblesH = row[11]
      g.sackYdsH = row[12]
      g.penYdsH = row[13]
      g.timePosH = timeToSeconds(row[14])
      g.teamA = row[16]
      g.scoreA = row[17]
      g.firstDownA = row[18]
      g.thirdDownPctA = float(row[19][0:-1]) / 100
      g.rushAttA = row[20]
      g.rushYdsA = row[21]
      g.passAttA = row[22]
      g.passCompA = row[23]
      g.passYdsA = row[24]
      g.passIntA = row[25]
      g.fumblesA = row[26]
      g.sackYdsA = row[27]
      g.penYdsA = row[28]
      g.timePosA = timeToSeconds(row[29])
      g.line = 0 - float(row[31])
    elif row[30] == 'V':
      g.teamA = row[1]
      g.scoreA = row[2]
      g.firstDownA = row[3]
      g.thirdDownPctA = float(row[4][0:-1]) / 100
      g.rushAttA = row[5]
      g.rushYdsA = row[6]
      g.passAttA = row[7]
      g.passCompA = row[8]
      g.passYdsA = row[9]
      g.passIntA = row[10]
      g.fumblesA = row[11]
      g.sackYdsA = row[12]
      g.penYdsA = row[13]
      g.timePosA = timeToSeconds(row[14])
      g.teamH = row[16]
      g.scoreH = row[17]
      g.firstDownH = row[18]
      g.thirdDownPctH = float(row[19][0:-1]) / 100
      g.rushAttH = row[20]
      g.rushYdsH = row[21]
      g.passAttH = row[22]
      g.passCompH = row[23]
      g.passYdsH = row[24]
      g.passIntH = row[25]
      g.fumblesH = row[26]
      g.sackYdsH = row[27]
      g.penYdsH = row[28]
      g.timePosH = timeToSeconds(row[29])
      g.line = float(row[31])
    elif row[30] == 'N':
      ignored += 1
      print "Neutral site game, continuing..."
      continue
    elif row[30] == '':
      print "Empty row, continuing..."
      continue
    else:
      raise Exception("Unexpected value for site: " + row[30])
  else:
    if row[32] == 'H':
      g.teamH = row[1]
      g.scoreH = row[2]
      g.firstDownH = row[3]
      g.thirdDownPctH = float(row[4][0:-1]) / 100
      g.rushAttH = row[5]
      g.rushYdsH = row[6]
      g.passAttH = row[7]
      g.passCompH = row[8]
      g.passYdsH = row[9]
      g.passIntH = row[10]
      g.fumblesH = row[11]
      g.sackYdsH = row[13]
      g.penYdsH = row[14]
      g.timePosH = timeToSeconds(row[15])
      g.teamA = row[17]
      g.scoreA = row[18]
      g.firstDownA = row[19]
      g.thirdDownPctA = float(row[20][0:-1]) / 100
      g.rushAttA = row[21]
      g.rushYdsA = row[22]
      g.passAttA = row[23]
      g.passCompA = row[24]
      g.passYdsA = row[25]
      g.passIntA = row[26]
      g.fumblesA = row[27]
      g.sackYdsA = row[29]
      g.penYdsA = row[30]
      g.timePosA = timeToSeconds(row[31])
      g.line = 0 -float(row[33])
    elif row[32] == 'V':
      g.teamA = row[1]
      g.scoreA = row[2]
      g.firstDownA = row[3]
      g.thirdDownPctA = float(row[4][0:-1]) / 100
      g.rushAttA = row[5]
      g.rushYdsA = row[6]
      g.passAttA = row[7]
      g.passCompA = row[8]
      g.passYdsA = row[9]
      g.passIntA = row[10]
      g.fumblesA = row[11]
      g.sackYdsA = row[13]
      g.penYdsA = row[14]
      g.timePosA = timeToSeconds(row[15])
      g.teamH = row[17]
      g.scoreH = row[18]
      g.firstDownH = row[19]
      g.thirdDownPctH = float(row[20][0:-1]) / 100
      g.rushAttH = row[21]
      g.rushYdsH = row[22]
      g.passAttH = row[23]
      g.passCompH = row[24]
      g.passYdsH = row[25]
      g.passIntH = row[26]
      g.fumblesH = row[27]
      g.sackYdsH = row[28]
      g.penYdsH = row[29]
      g.timePosH = timeToSeconds(row[31])
      g.line = float(row[33])
    elif row[32] == 'N':
      ignored += 1
      print "Neutral site game, continuing.."
      continue
    elif row[32] == '':
      print "Empty row, continuing..."
      continue
    else:
      raise Exception("Unexpected value for site: " + row[32])
  already = Game.objects.filter(date = g.date, teamA = g.teamA, teamH = g.teamH)
  if already.count() == 1:
    dups += 1
    notduplicated.remove((g.teamA, g.teamH, g.date))
    print "Already in database: " + g.teamA + " at " + g.teamH + " on " + g.date
  elif already.count() == 0:
    games += 1
    notduplicated.append((g.teamA, g.teamH, g.date))
    if g.teamA == g.teamH:
      teamteam.append(g.date)
    else:
      print "Saved game: " + g.teamA + " at " + g.teamH + " on " + g.date
      g.save()
  else:
    raise Exception("Duplicate game in there")

print "Finished with " + str(games) + " games saved to the database, " + str(dups) + " duplicates ignored, and " + str(ignored/2) + " neutral site games ignored"

for tt in teamteam:
  print "Ignored a game in week " + tt + " because of faulty data (teamx at teamx)"

print "The following games only appeared once in the csv: "
for nd in notduplicated:
  print nd
