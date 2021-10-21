import os 
import sys
"""
Deletes all labels with @label_name in all subfolders of @source_folder (given the same file-structure in @source_folder as for labels/features)

"""
def delete_labels(source_folder, label_name):
    leagues = os.listdir(source_folder)
    for league in leagues:
        league_path = source_folder + "/" + league
        if league_path.endswith("DS_Store"):
            continue
        seasons = os.listdir(league_path)
        for season in seasons:
            season_path = league_path + "/" + season
            if season_path.endswith("DS_Store"):
                continue
            matches = os.listdir(season_path)
            for match in matches:
                match_path = season_path + "/" + match
                if match_path.endswith("DS_Store"):
                    continue
                file_path = match_path + "/" + label_name
                if os.path.isfile(file_path):
                    os.remove(file_path)
                else:
                    print("{} does not exist.".format(file_path))


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3:
        print(f"2 command line arguments expected, {len(args) - 1} found")
        exit()
    
    source = args[1]
    label_name = args[2]

    delete_labels(source, label_name)