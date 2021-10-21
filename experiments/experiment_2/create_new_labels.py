import json
import os
import sys
"""
Changes labels to match requirements of experiment 2. Takes one argument @source: 
root folder of features/labels. Parent-folder of leagues. 
"""
def create_labels_next(filepath):
    split = filepath.split("/")
    
    # filepath = os.path.abspath(filepath)
    
    file = open(filepath)
    write_filepath = filepath.replace(split[-1], "Labels-v2-next.json")
    write_file = open(write_filepath, "x")
    labels = json.load(file)
    
    for i in range(len(labels["annotations"]) - 1):
        current = labels["annotations"][i]
        next = labels["annotations"][i+1]
        half_current = current["gameTime"][0]
        half_next = next["gameTime"][0]
        if half_current != half_next:
            continue
        current["label"] = next["label"]
    
    json.dump(labels, write_file)
    file.close()
    write_file.close()


def create_labels_previous(filepath):
    split = filepath.split("/")

    # filepath = os.path.abspath(filepath)

    file = open(filepath)
    write_filepath = filepath.replace(split[-1], "Labels-v2-previous.json")
    write_file = open(write_filepath, "x")
    labels = json.load(file)
    for i in range(len(labels["annotations"]) - 1, -1, -1):
        current = labels["annotations"][i]
        previous = labels["annotations"][i-1]
        half_current = current["gameTime"][0]
        half_previous = previous["gameTime"][0]
        if half_current != half_previous:
            continue
        current["label"] = previous["label"]

    for i in range(len(labels["annotations"]) - 1):
        half = labels["annotations"][i]["gameTime"][0]
        if half == '2':
            labels["annotations"].pop(i)
            break

    labels["annotations"] = labels["annotations"][1:]

    json.dump(labels, write_file)
    file.close()
    write_file.close()


def create_new_labels(source):
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
                create_labels_previous(source_filepath)
                create_labels_next(source_filepath)


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        print(f" 1 command line argument expected, {len(args) - 1} found")
        exit()

    source = args[1]

    create_new_labels(source)