import copy
events_1 = [
    {
        "gameTime": "1 - 35:39",
        "label": "Penalty",
        "position": "23000",
        "half": "1",
        "confidence": "0.5"
    },
    {
        "gameTime": "1 - 35:39",
        "label": "Goal",
        "position": "230300",
        "half": "1",
        "confidence": "0.2"
    },
    {
        "gameTime": "1 - 35:39",
        "label": "Penalty",
        "position": "23500",
        "half": "1",
        "confidence": "0.9"
    },
    {
        "gameTime": "1 - 35:39",
        "label": "Goal",
        "position": "29000",
        "half": "1",
        "confidence": "0.1"
    }
]
events_2 = [
    {
        "gameTime": "1 - 35:39",
        "label": "Goal",
        "position": "29500",
        "half": "1",
        "confidence": "0.5"
    },
    {
        "gameTime": "1 - 35:39",
        "label": "Clearance",
        "position": "30500",
        "half": "1",
        "confidence": "0.5"
    },
    {
        "gameTime": "1 - 35:39",
        "label": "Clearance",
        "position": "30600",
        "half": "1",
        "confidence": "0.1"
    }
]
events_3 = []


def get_preds_within_window(min_pos, max_pos, preds, half):
    return [p for p in preds if int(p["position"]) >= min_pos and int(p["position"]) <= max_pos and int(p["gameTime"][0]) == half]

def get_most_confident_preds(min_pos, max_pos, past_p, current_p, future_p, half):
    #First we have to get the relevant events within timewindow: 
    past_p = get_preds_within_window(min_pos, max_pos, past_p, half)
    current_p = get_preds_within_window(min_pos, max_pos, current_p, half)
    future_p = get_preds_within_window(min_pos, max_pos, future_p, half)

    #Put them in the right bins: 
    prediction_bins = {
        "Throw-in": [],
        "Ball out of play": [],
        "Kick-off": [],
        "Indirect free-kick": [],
        "Clearance": [],
        "Foul": [],
        "Corner":[],
        "Substitution": [],
        "Offside": [],
        "Direct free-kick": [],
        "Yellow card": [],
        "Shots on target": [],
        "Shots off target": [],
        "Goal": [],
        "Red card": [],
        "Penalty": [],
        "Yellow->red card": []
    }
    for p in past_p:
        prediction_bins[p["label"]].append(p)
    for p in current_p: 
        prediction_bins[p["label"]].append(p)
    for p in future_p:
        prediction_bins[p["label"]].append(p)
    
    for k in prediction_bins.keys():
        prediction_bins[k].sort(key=lambda p: float(p["confidence"]), reverse=True)
    
    candidate_preds = []
    for k in prediction_bins.keys():
        if len(prediction_bins[k]) > 0:
            candidate_preds.append(prediction_bins[k][0])
    return candidate_preds

def filter_on_confidence(t_window, past_p, current_p, future_p): #Returns a list of predictions after filtering on confidence, according to 5.2
    confident_preds = []
    #Iterate over t_window from 0:00 to 50:00 for both halves of a match. 
    #For a given window t_window: Gather all events from all predictions into separate "bins". Remove every one, but the one with the most confidence
    t_window = t_window * 1000
    #half 1:
    for i in range(0, 3000000, t_window): 
        min_i = i
        max_i = i + t_window
        print("min_i: {}".format(min_i))
        print("max_i: {}".format(max_i))
        preds_in_window = get_most_confident_preds(min_i, max_i,past_p, current_p, future_p, 1)
        if len(preds_in_window) > 0:
            for p in preds_in_window:
                confident_preds.append(p)
    #for second half:
    for i in range(0, 300000, t_window):
        min_i = i
        max_i = i + t_window
        preds_in_window = get_most_confident_preds(min_i, max_i,past_p, current_p, future_p, 2)
        if len(preds_in_window) > 0:
            for p in preds_in_window:
                confident_preds.append(p)
    return confident_preds

print(filter_on_confidence(2, events_1, events_2, events_3))

