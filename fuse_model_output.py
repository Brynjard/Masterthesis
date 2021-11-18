import os 
import sys
"""
results_spotting.json
"""
def create_file_structure(model_output_src, fuse_output_dir):
    if os.path.isdir(model_output_src) != True or os.path.isdir(fuse_output_dir) != True:
        print("ERROR: One of the supplied folders does not exist.")
    


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
                continue"""