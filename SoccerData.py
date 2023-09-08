import requests
import json

apiKey = "da6fc67156e34b5580ff508b05945c9f"

selectedID = ""
selectedURI = ""
ENGuri = "http://api.football-data.org/v4/competitions/PL/standings"
GERuri = "http://api.football-data.org/v4/competitions/BL1/standings"
ITAuri = "http://api.football-data.org/v4/competitions/SA/standings"
FRAuri = "http://api.football-data.org/v4/competitions/FL1/standings"

leagues = ["England", "Germany", "Italy", "France", "Spain"]
leagueIDs = {"England": "PL", "Germany": "BL1", "Italy": "SA", "France": "FL1", "Spain": "PD", "UEFA Champions League": "CL"}


# User inputs which league they want to see the standings for and the program checks to see if its a valid league
active = True
while active == True:
    leagueValidation = False
    while leagueValidation == False:
        print("LEAGUES AVAILABLE:")
        for league in leagues:
            print(league)

        print("")
        competition = input("Which League would you like to see the standings for?    ")

        if competition in leagues:
            selectedID = leagueIDs[competition]
            selectedURI = f"http://api.football-data.org/v4/competitions/{selectedID}/standings"
            leagueValidation = True
        else:
            print("Not a valid league, try again")
            print("")

    # Make API request and return a json file of the selected league
    headers = { 'X-Auth-Token': apiKey }
    response = requests.get(selectedURI, headers=headers)

    # Retreiving the league name and season year
    leagueYear = response.json()["season"]["startDate"][:4]
    leagueName = response.json()["competition"]["name"]

    # Retrieving raw League Table with every stat available
    rawLeagueTable = response.json()["standings"][0]["table"]

    # Creating new league table dictionary with only the stats I want
    filteredLeagueTable = {}
    for team in rawLeagueTable:
        rank = team["position"]
        name = team["team"]["name"]
        wins = team["won"]
        draws = team["draw"]
        losses = team["lost"]
        points = team["points"]
        filteredLeagueTable[name] = {"rank": rank, 
                                    "wins": wins,  
                                    "draws": draws, 
                                    "losses": losses, 
                                    "points": points}
        
    # Finding largest team name length
    longestTeam = ""
    for team in filteredLeagueTable:
        if len(team) > len(longestTeam):
            longestTeam = team

    length = int(len(longestTeam))

    # Printing new league table
    print(f"{'':-<60}")
    print(leagueName + " " + str(leagueYear) + " Season Standings")
    print(f"{'':-<60}")
    print(f"{'Rank': <5}{'Team Name': <28}{'W': <5}{'D': <5}{'L': <5}{'Points'}")

    for team in filteredLeagueTable:
        print(f"{filteredLeagueTable[team]['rank']: <5}{team: <28}{filteredLeagueTable[team]['wins']: <5}{filteredLeagueTable[team]['draws']: <5}{filteredLeagueTable[team]['losses']: <5}{filteredLeagueTable[team]['points']: <5}")
    
    print("")
    activeCheck = input("Would you like to look up another league? Yes/No    ")

    if activeCheck =="yes" or activeCheck == "Yes":
        print("")
        leagueValidation = False
    else:
        print("Thank You")
        active = False
