#!/usr/bin/python3

import json

with open('players.json') as user_file:
  parsed_json = json.load(user_file)
  
new_dict = {}

for keys in parsed_json:
    entry = parsed_json[keys]
    
    # make tuple into one string as tuple and write 
    if(keys.isdigit()):
        new_dict["{0} {1}".format(entry["first_name"], entry["last_name"]), entry["team"], entry["position"]] = entry
        new_dict["{0} {1}".format(entry["first_name"], entry["last_name"]), entry["team"], entry["position"]]["id"] = keys
    else:
        new_dict[keys] = entry
    
final_dict = {}
for items in new_dict:
    if len(items[0]) == 1:
        final_dict[items] = new_dict[items]
    else:
        tuple_key = "{0},{1},{2}".format(items[0], items[1], items[2])
        final_dict[tuple_key] = new_dict[items]

with open("players_to_id.json", mode='w') as json_file:
    json.dump(final_dict, json_file, indent=4)
    
    