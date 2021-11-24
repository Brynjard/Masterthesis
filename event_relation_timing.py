import json
import os
import sys
import statistics
from numpy.lib.function_base import average, median
"""
Calculates the time between different events. This is used for action grounding for next and
previous models in different experiments. Takes one argument @source, which is the
root folder of features/labels. Parent-folder of leagues. 
"""

events_dict_past = {
    "Throw-in": ["Ball out of play"],
    "Kick-off": ["Goal"],
    "Indirect free-kick": ["Foul", "Offside"],
    "Clearance": ["Ball out of play"],
    "Corner": ["Ball out of play"],
    "Direct free-kick": ["Foul"],
    "Yellow card": ["Foul"],
    "Red card": ["Foul"]
}

events_dict_future = {
    "Ball out of play": ["Throw-in", "Clearance", "Corner"],
    "Foul": ["Indirect free-kick", "Direct free-kick", "Yellow card", "Red card"],
    "Offside": ["Indirect free-kick"],
    "Goal": ["Kick-off"]
}

event_time_past = {
    "Throw-in": [],
    "Kick-off": [],
    "Indirect free-kick": [],
    "Clearance": [],
    "Corner": [],
    "Direct free-kick": [],
    "Yellow card": [],
    "Red card": []
}

event_time_future = {
    "Ball out of play": [],
    "Foul": [],
    "Offside": [],
    "Goal": []
}

def get_avg_time_between_events(filepath):
    
    file = open(filepath)
    
    labels = json.load(file)
    for i in range(len(labels["annotations"]) - 1):
        current_event = labels["annotations"][i]
        current_event_name = current_event["label"]
        if current_event_name in events_dict_past.keys():
            # ## Events:
            associated_events = events_dict_past[current_event_name]
             
            ## Go backward to find one of the events in
            event_position = find_associated_event(current_event, i, labels, associated_events, -1)
            if event_position == -1:
                continue
            else:
                time_between_events = abs(int(current_event["position"]) - event_position)
                time_list = event_time_past[current_event_name]
                time_list.append(time_between_events)
                event_time_past[current_event_name] = time_list

        elif current_event_name in events_dict_future.keys():
            
            associated_events = events_dict_future[current_event_name]

            ## Go forward to find one of the events
            event_position = find_associated_event(current_event, i, labels, associated_events, 1)
            if event_position == -1:
                continue
            else:
                time_between_events = abs(int(current_event["position"]) - event_position)
                time_list = event_time_future[current_event_name]
                time_list.append(time_between_events)
                event_time_future[current_event_name] = time_list

    file.close()

def find_associated_event(current_event, start_index, labels, associated_events, step):
    for i in range(1 * step, 3 * step, step):
        if i == 5 or i == -5:
            print(f" {current_event['label']} {i}")
        if start_index + (i * step) < 0 or start_index + (i * step) > len(labels["annotations"]) - 1:
            return -1
        event = labels["annotations"][start_index + (i * step)]
        if event["label"] == current_event["label"]:
            return -1
        elif event["gameTime"][0] != current_event["gameTime"][0]:
            return -1
        elif event["label"] in associated_events:
            return int(event["position"])
    return -1


def calculate_time_between_events(source):
    leagues = os.listdir(source)
    for league in leagues:
        seasons_path = source + "/" + league
        if seasons_path.endswith("DS_Store"):
            continue
        seasons = os.listdir(seasons_path)
        for season in seasons:
            matches_path = source + "/" + league + "/" + season
            if matches_path.endswith("DS_Store"):
                continue
            matches = os.listdir(matches_path)
            for match in matches:
                match_path = league + "/" + season + "/" + match
                if match_path.endswith("DS_Store"):
                    continue
                source_filepath = source + "/" + match_path + "/" + "Labels-v2.json"
                if source_filepath.endswith("DS_Store"):
                    continue
                if os.path.isfile(source_filepath):
                    get_avg_time_between_events(source_filepath)


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:

        print(f" 1 command line argument expected, {len(args) - 1} found")
        print(f"The argument should be the root folder of the labels.")
        exit()

    source = args[1]
    calculate_time_between_events(source)

    # Calculate average time

    print(f"\nTime from next event to 'previous' event:")
    for key, value in event_time_past.items():
        if len(value) != 0:
            min_time = min(value)
            max_time = max(value)
            avg_time = average(value)
            median_time = median(value)
            print(f"{key}")
            print(f"avg {round(avg_time, 1)} --- avg(sec) {round(avg_time / 1000, 1)} --- median {median_time} --- median (sec) {round(median_time / 1000, 1)} --- min {min_time} --- max {max_time} --- n {len(value)}")
        else:
            print(f"{key} --- No data ---" )
            
    print(f"\nTime from previous event to 'next' event:")
    for key, value in event_time_future.items():
        if len(value) != 0:
            min_time = min(value)
            max_time = max(value)
            avg_time = average(value)
            median_time = median(value)
            print(f"{key}")
            print(f"avg {round(avg_time, 1)} --- avg(sec) {round(avg_time / 1000, 1)} --- median {median_time} --- median (sec) {round(median_time / 1000, 1)} --- min {min_time} --- max {max_time} --- n {len(value)}")
        else:
            print(f"{key} --- No data ---" )