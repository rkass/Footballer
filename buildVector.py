import math
import settings
from django.core.management import setup_environ
setup_environ(settings)
from stats.models import Game
import sys 

#Returns true if the two games are in the same season, false otherwise
def sameSeason(game, game2):
  year1, year2 = game.date.year, game2.date.year
  if game.date.month < 3:
    year1 -= 1
  if game2.date.month < 3:
    year2 -= 1
  return year1 == year2  

#Returns the last game for team (either home or away) this season
#Returns none if no such game exists 
def getLastGame(game, team):
  away, home = None, None
  if team == 'away':  
    if Game.objects.filter(date__lt = game.date, teamA = game.teamA).count() > 0:
      away = Game.objects.filter(date__lt = game.date, teamA = game.teamA).latest('date')
    if Game.objects.filter(date__lt = game.date, teamH = game.teamA).count() > 0:
      home = Game.objects.filter(date__lt = game.date, teamH = game.teamA).latest('date')
  elif team == 'home':
    if Game.objects.filter(date__lt = game.date, teamA = game.teamH).count() > 0:
      away = Game.objects.filter(date__lt = game.date, teamA = game.teamH).latest('date')
    if Game.objects.filter(date__lt = game.date, teamH = game.teamH).count() > 0:
      home = Game.objects.filter(date__lt = game.date, teamH = game.teamH).latest('date')
  else:
    raise Exception("Unexpected value for team")
  if away == None and home != None:
    return home
  if home == None and away != None:
    return away
  if home == None and away == None:
    return None
  if away.date > home.date:
    if sameSeason(away, game):
      return away
    else:
      return None
  else:
    if sameSeason(home, game):
      return home
    else:
      return None

#Returns a list of the last three game objects
#If the game's week is < 4, it returns None
def getLastThreeGames(game, team):
  team = team
  game = game
  ret = ([], [])
  x = 0
  while(x < 3):
    lastGame = getLastGame(game, team)
    if lastGame == None:
      return (None, None)
    ret[0].append(lastGame)
    if team == 'away':
      oldTeamName = game.teamA
    else:
      oldTeamName = game.teamH
    game = lastGame
    if oldTeamName == game.teamA:
      team = 'away'
      notTeam = 'home'
    else:
      team = 'home'
      notTeam = 'away'
    ret[1].append(notTeam)
    x += 1
  return ret

#Takes a game and the name of the target team and turns
#it into a sixth vector defined by the vectors file
def gameToVector(game, team):
  ret = []
  ret.append(game.scoreA)  
  ret.append(game.firstDownA)
  ret.append(game.thirdDownPctA)
  ret.append(game.rushAttA)
  ret.append(game.rushYdsA)
  ret.append(game.passAttA)
  ret.append(game.passYdsA)
  ret.append(game.passIntA)
  ret.append(game.fumblesA)
  ret.append(game.sackYdsA)
  ret.append(game.penYdsA)
  ret.append(game.timePosA)
  ret.append(game.scoreH)
  ret.append(game.firstDownH)
  ret.append(game.thirdDownPctH)
  ret.append(game.rushAttH)
  ret.append(game.rushYdsH)
  ret.append(game.passAttH)
  ret.append(game.passYdsH)
  ret.append(game.passIntH)
  ret.append(game.fumblesH)
  ret.append(game.sackYdsH)
  ret.append(game.penYdsH)
  ret.append(game.timePosH)
  if game.teamA == team:
    ret.append(0)
  else:
    ret = ret[12:] + ret[0:12]
    ret.append(1)
  return ret
    
#Takes a list of three games ordered most recent first
#and turns it into a vector defined by the vectors file
def threeGamesToVector(glist):
  lst = [glist[0].teamA, glist[1].teamA, glist[2].teamA, glist[0].teamH,
         glist[1].teamH, glist[2].teamH]
  team = max(set(lst), key=lst.count)
  assert lst.count(team) == 3
  return gameToVector(glist[0], team) + gameToVector(glist[1], team) + gameToVector(glist[2], team)

#> 0 for home, < 0 for away, 0 for push
def decideBettingWinner(game):
  return game.scoreH + game.line - game.scoreA

#Returns a list of labeled training examples. 1 if home team covered, -1 if away team covered
#Pushes omitted
def genVectors():
  vects = []
  games = Game.objects.all()
  first = True
  count = 0
  for game in games:
    count += 1 
    if count % 100 == 0:
      print "HHEEEYYYY" + str(count)
    if first:
      first = False
      continue
    (lta, site) = getLastThreeGames(game, 'away')
    if lta != None:
      (lta1, _) = getLastThreeGames(lta[0], site[0])
      (lta2, _) = getLastThreeGames(lta[1], site[1])
      (lta3, _) = getLastThreeGames(lta[2], site[2])
    (lth, site) = getLastThreeGames(game, 'home')
    if lth != None:
      (lth1, _) = getLastThreeGames(lth[0], site[0])
      (lth2, _) = getLastThreeGames(lth[1], site[1])
      (lth3, _) = getLastThreeGames(lth[2], site[2])
    linedScore = decideBettingWinner(game)
    if lta != None and lth != None and lta1 != None and lta2 != None and lta3 != None and lth1 != None and lth2 != None and lth3 != None and linedScore != 0:
      vect = threeGamesToVector(lta) + threeGamesToVector(lta1) + threeGamesToVector(lta2) + threeGamesToVector(lta3) + threeGamesToVector(lth) + threeGamesToVector(lth1) + threeGamesToVector(lth2) + threeGamesToVector(lth3)
      if linedScore > 0:
        vects.append((vect, 1))
      else:
        vects.append((vect, -1))
  return vects
      
def normalizeSet(lst):
  mean = float(sum(lst)) / len(lst)
  variance = 0
  for el in lst:
    variance += (el - mean)**2
  variance = variance / len(lst)
  sd = math.sqrt(variance) 
  retlst = []
  for el in lst:
    retlst.append((el - mean) / sd)
  return retlst

#takes a list of lists and normalizes index i according to
#all elements with index i in these lists
def normalizeIndex(lst, i):
  s = []
  for l,c in lst:
    s.append(l[i])
  s = normalizeSet(s)[::-1]
  for l,c in lst:
    l[i] = s.pop()

def mean(lst):
  tot = 0.
  for x in lst:
    tot += x
  return tot/float(len(lst))

def sd(lst):
  mn = mean(lst)
  var = 0
  for x in lst:
    var += (x - mn)**2
  var = var/float(len(lst))
  return var**(.5)

def normalizeVectors(vects):
  indexVects = []
  b = 0
  while b < len(vects[0][0]):
    indexVects.append([])
    b += 1
  means = []
  sds = []
  for tup in vects:
    v = tup[0]
    count = 0
    while count < len(v):
      indexVects[count].append(v[count])
      count += 1
  for iv in indexVects:
    m = mean(iv)
    s = sd(iv)
    means.append(m) 
    sds.append(s)
  for tup in vects:
    index = 0
    while index < len(tup[0]):
      tup[0][index] = (float(tup[0][index]) - means[index])/sds[index]
      index += 1
  return vects
    
    
      


      
