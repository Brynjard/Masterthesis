import sys
from modify_labels_utils import create_event_dict_for_future_model, create_event_dict_for_past_model, create_label_dict

EVENT_DICT = {
    "Ball out of play": 0,
    "Throw-in": 0,
    "Kick-off": 0,
    "Indirect free-kick": 0,
    "Clearance": 0,
    "Foul": 0,
    "Corner": 0,
    "Substitution": 0,
    "Offside": 0,
    "Direct free-kick": 0,
    "Yellow card": 0,
    "Shots on target": 0,
    "Shots off target": 0,
    "Goal": 0,
    "Red card": 0,
    "Penalty": 0,
    "Yellow->red card": 0
}

def get_event_dict() -> dict:
    return {
        "Ball out of play": 0,
        "Throw-in": 0,
        "Kick-off": 0,
        "Indirect free-kick": 0,
        "Clearance": 0,
        "Foul": 0,
        "Corner": 0,
        "Substitution": 0,
        "Offside": 0,
        "Direct free-kick": 0,
        "Yellow card": 0,
        "Shots on target": 0,
        "Shots off target": 0,
        "Goal": 0,
        "Red card": 0,
        "Penalty": 0,
        "Yellow->red card": 0
        }

def get_total_annotations(label_dict):
    total_annotations = 0
    for filename in label_dict.keys():
        total_annotations += len(label_dict[filename]["annotations"])
    return total_annotations


def get_annotations_per_class(label_dict) -> dict:
    event_dict = get_event_dict()
    for filename in label_dict.keys():
        for annotation in label_dict[filename]["annotations"]:
            label = annotation["label"]
            count = event_dict.get(label)
            event_dict[label] = count + 1
    return event_dict

def print_dict(event_dict):
    for key, value in event_dict.items():
        print("{:<20}: {:>10}".format(key, value))


if __name__ == '__main__':
    args = sys.argv
    
    ## "source" should be the "original features folder"
    source = args[1]

    ## Run following functions

    ## Get current labels
    current_dict = create_label_dict(source, "Labels-v2.json")
    print(f"Total number of current labels: {get_total_annotations(current_dict)}")
    event_dict_current = get_annotations_per_class(current_dict)
    print_dict(event_dict_current)
    
    print("")

    ## Get past labels
    past_dict = create_label_dict(source, "Labels-v2-past-ex4.json")
    print(f"Total number of past labels: {get_total_annotations(past_dict)}")
    event_dict_past = get_annotations_per_class(past_dict)
    print_dict(event_dict_past)

    print("")

    ## Get future labels
    future_dict = create_label_dict(source, "Labels-v2-future-ex4.json")
    print(f"Total number of future labels: {get_total_annotations(future_dict)}")
    event_dict_future = get_annotations_per_class(future_dict)
    print_dict(event_dict_future)


    ## Count total data per class:

    


