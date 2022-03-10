import os 
import sys
"""
Deletes all labels with @label_name in all subfolders of @source_folder (given the same file-structure in @source_folder as for labels/features)

"""

def delete_files(source, file_name):
    if os.path.isfile(source):
        if source == file_name:
            os.remove(source)
    else:
        sub_entries = os.listdir(source)
        for entry in sub_entries:
            path = source + "/" + entry
            if entry == file_name:
                os.remove(path)
            elif os.path.isdir(path):
                delete_files(path, file_name)
            else:
                continue


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3:
        print(f"2 command line arguments expected, {len(args) - 1} found")
        exit()

    source = args[1]
    label_name = args[2]
    confirmation = input(f"WARNING: This will delete all files with name: '{label_name}' in source folder and all its sub-folders. Continue? (yes/[no]):\n")
    if confirmation == "yes":
        delete_files(source, label_name)
