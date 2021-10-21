import os
import sys
from shutil import copyfile

def move_labels(source, destination):
    leagues = os.listdir(source)
    for league in leagues:
        seasons_path = source + "/" + league
        seasons = os.listdir(seasons_path)
        for season in seasons:
            matches_path = source + "/" + league + "/" + season
            matches = os.listdir(matches_path)
            for match in matches:
                match_path = league + "/" + season + "/" + match
                source_filepath = source + "/" + match_path + "/" + "Labels-v2.json"
                destination_filepath  = destination + "/" + match_path + "/" + "Labels-v2.json"
                copyfile(source_filepath, destination_filepath)


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3:
        print(f"2 command line arguments expected, {len(args) - 1} found")
        exit()
    
    source = args[1]
    destination = args[2]

    move_labels(source, destination)
