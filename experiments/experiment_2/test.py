import os
from collections import defaultdict, Counter
import json
from shutil


def convert_to_previous_labels(orig_labels_path, new_labels_path):
    shutil.copyfile(orig_labels_path, new_labels_path)

    
    

