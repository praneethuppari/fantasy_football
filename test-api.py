import requests
import json
from queue import Queue
from typing import Literal, get_args
import csv
import time

rankingTypes = Literal["positionless", "position"]

with open('players_to_id.json', mode='r') as players_json:
    players = json.load(players_json)
    
drafted = []

draftQueue = Queue(maxsize=0) # infinite queue, probably going to use priority queue in the future

def processDraftRankings(file_path: str, rankings_type: rankingTypes = "positionless"):
    
    options = get_args(rankingTypes)
    if rankings_type not in options:
        raise Exception("Invalid rankings type was given. Must be 'positionless' or 'positions'")
    
    with open('FantasyPros_2023_Draft_ALL_Rankings.csv', mode='r') as csv_file:
        csv_draft_queue = csv.DictReader(csv_file)
        for row in csv_draft_queue:
            addToDraftQueue(row)
    

def addToDraftQueue(player: dict):
    player_team = player.get("TEAM")
    if(player_team == "FA"):
        player_team = "None"
    
    key_to_dict = ''
    player_pos = player.get("POS")
    
    if(player_pos[0:2] == "DS"):
        key_to_dict = player_team
    else:
        end_rank = 2
        if(player_pos[0:1] == "K"):
            end_rank = 1
        key_to_dict = "{0},{1},{2}".format(player.get("PLAYER NAME"), player_team, player.get("POS")[0:end_rank])
    
    player_id = players[key_to_dict].get("id", player_team)
    if(player_id == "-1"):
        print("This guy does not have id ", key_to_dict)
    draftQueue.put(player_id)

def get_player():
    
    player = draftQueue.get()
    while(player in drafted):
        player = draftQueue.get()
        print(player)
        
    return player
    
        
        
    
def run_draft(pick_number):
    DRAFT_ID = 988670358830084096
    
    latest_pick = 0
    while(latest_pick != 180):
        response = requests.get('https://api.sleeper.app/v1/draft/{0}/picks'.format(DRAFT_ID)).json()
        for x in range(latest_pick, len(response)):
            drafted.append(response[x].get("player_id"))
            latest_pick = latest_pick + 1
            print(latest_pick)
        
        print(response[latest_pick-1])
        if (latest_pick > 0):
            
            if (response[latest_pick-1].get("round") % 2 == 1):
                
                print(response[latest_pick-1].get("pick_no") % 12 == (pick_number-1))
            
                if response[latest_pick-1].get("pick_no") % 12 == (pick_number-1): 
            
                        player = get_player()
                        print("Draft player: ", player)
                        while(response[latest_pick-1].get("pick_no") == latest_pick):
                            time.sleep(60)
        

        time.sleep(1)
    
    print(drafted)
        
        
            

def main():
    processDraftRankings('player_rankings.csv', 'position')
    run_draft(9)

if __name__ == "__main__":
    main()
    
    



LEAGUE_ID = 987176400224370688


#response = requests.get('https://api.sleeper.app/v1/draft/{0}/picks'.format(DRAFT_ID))

#draft_queue = {
 #   1: "Ja'Marr Chase",
 #   2: "Cooper Kupp",
 #   3: "Tom Brady"
#}

#queue = [
#]

'''
To Do:
1. Process a CSV File with rankings 
   - convert all players in csv file into player IDs
   - add them to queues 
    - Options for player CSVs, 
    1) queues for each position with data
    2) 1 singular queue --> focus on this first
2. Call the api every 45 seconds and update the drafted queue --> every % players, pop off of queues 
    - 
'''


#users = response.json()

#for user in users:
#    print("Pick {0}.{1}, player drafted is {2} {3}".format(
#          user.get('round'), 
#         user.get('draft_slot'), 
#         user['metadata'].get('first_name'), 
#         user['metadata'].get('last_name')))
#   queue.append(user['metadata'].get('first_name'))
# print(queue)