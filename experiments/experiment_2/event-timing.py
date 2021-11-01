import json
import os
import sys
"""
Calculates the average time between events. This is used for action grounding for next and
previous models in experiment 2. Takes one argument @source, which is the
root folder of features/labels. Parent-folder of leagues. 
"""

def get_avg_time_between_events(filepath):
    
    file = open(filepath)
    
    labels = json.load(file)
    total_time_between_events = 0
    total_events = 0
    for i in range(len(labels["annotations"]) - 1):
        current = labels["annotations"][i]
        next = labels["annotations"][i+1]
        half_current = current["gameTime"][0]
        half_next = next["gameTime"][0]
        if half_current != half_next:
            continue
        current_position = current["position"]
        next_position = next["position"]

        total_time_between_events += int(next_position) - int(current_position)
        total_events += 1

    file.close()
    return total_time_between_events / total_events

def calculate_time_between_events(source):
    leagues = os.listdir(source)
    avg_time_per_match = 0 
    number_of_matches = 0
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
                avg_time_per_match += get_avg_time_between_events(source_filepath)
                number_of_matches += 1

    return avg_time_per_match/number_of_matches


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        print(f" 1 command line argument expected, {len(args) - 1} found")
        print(f"The argument should be the root folder of the labels.")
        exit()

    source = args[1]
    average_time = calculate_time_between_events(source)

    print(f"Average time between events: {round(average_time, 2)} milliseconds.")

    