import os
import sys
from shutil import move

"""
Moves labels with a given @filename from @destination to @source according to the filestructure in source (league/season/match)
So that if we want to move labels into features, the labels for a match will be put in the same folder as the features for that match. 
"""

def move_labels(source, destination, filename):
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
                source_filepath = source + "/" + match_path + "/" + filename
                if os.path.isfile(source_filepath):
                    destination_filepath  = destination + "/" + match_path + "/" + filename
                    move(source_filepath, destination_filepath)


if __name__ == '__main__':
    args = sys.argv
    
    source = args[1]
    destination = args[2]
    filename = args[3]

    move_labels(source, destination, filename)
