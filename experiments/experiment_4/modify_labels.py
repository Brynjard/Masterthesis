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
    
    label_dict = utils.create_label_dict(label_src, "Labels-v2.json")
    ## Filter labels:
    future_dict = utils.create_event_dict_for_future_model(label_dict)
    past_dict = utils.create_event_dict_for_past_model(label_dict)
    
    # utils.print_events(label_dict)
    # utils.print_events(future_dict)
    # utils.print_events(past_dict)
    
    ## Create new labels for ex4:
    utils.write_annotations(future_dict, "Labels-v2-future-ex4-20220128.json")
    utils.write_annotations(past_dict, "Labels-v2-past-ex4-20220128.json")
