import os
import sys
from shutil import copyfile

"""
Moves label from @destination to @source according to the filestructure in source (liga/season/match)
So that if we want to move labels into features, the labels for a match will be put in the same folder as the features for that match. 
"""

def move_labels(source, destination):
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
                destination_filepath  = destination + "/" + match_path + "/" + "Labels-v21.json"
                copyfile(source_filepath, destination_filepath)


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3:
        print(f"2 command line arguments expected, {len(args) - 1} found")
        exit()
    
    source = args[1]
    destination = args[2]

    move_labels(source, destination)
