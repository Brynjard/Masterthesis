import sys, os, json

PARENT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(PARENT_FOLDER)
import modify_labels_utils as utils

"""
This script takes a src-folder from where we have the labels in ex2 (where each label is shifted timewise in accordance to past and future)
and filters these labels on what we know about which events each model can actually infer. Meaning that past-model does not contain
labels for kick-off for example, since we cannot infer that a kick-off happened in the past, based on what happens after the kick-off.
"""


if __name__ == '__main__':
    args = sys.argv
    label_src =  args[1]
    #Use labels from ex2. to create label-dictionaries:
    prev_dict = utils.create_label_dict(label_src, "Labels-v2-previous.json")
    next_dict = utils.create_label_dict(label_src, "Labels-v2-next.json")
    #Filter labels in accordance with ex3:
    utils.filter_events_for_next(next_dict)
    utils.filter_events_for_prev(prev_dict)
    #Create new labels for ex3:
    utils.write_annotations(next_dict, "Labels-v2-next-ex3.json")
    utils.write_annotations(prev_dict, "Labels-v2-previous-ex3.json")
