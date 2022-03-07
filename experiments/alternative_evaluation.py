import os
import numpy as np

from SoccerNet.utils import getListGames
from SoccerNet.Evaluation.utils import EVENT_DICTIONARY_V2, INVERSE_EVENT_DICTIONARY_V2

import json
from tqdm import tqdm
from collections import defaultdict

def evaluate_no_delta(SoccerNet_path, Predictions_path, confidence_threshold=0.0, prediction_file="results_spotting.json", split="test"):
    list_games = getListGames(split=split)

    """
    [
        "goal": {
            "True positive": 3,
            "False positive": 3,
            "False negative": 5,
        },
        "corner": {
            "True positive": 4,
            "False positive": 7,
            "False negative": 8,
        },
    ]
    """

    # Setup dict
    metric_dict = dict()
    for event_name in EVENT_DICTIONARY_V2.keys():
        metric_dict[event_name] = defaultdict(lambda: 0)

    for game in tqdm(list_games):
        
        # dict with predicion per class
        prediction_dict = defaultdict(lambda: 0)
        # dict with labels per class
        labels_dict = defaultdict(lambda: 0)

        ## Count labels per class
        label_files = "Labels-v2.json"
        labels = json.load(open(os.path.join(SoccerNet_path, game, label_files)))
        annotations = labels["annotations"]
        for annotation in annotations:
            label = annotation["label"]
            labels_dict[label] = labels_dict[label] + 1

        ## Count predicions per class
        predictions_file_dict = json.load(open(os.path.join(Predictions_path, game, prediction_file)))        
        predictions = predictions_file_dict["predictions"]
        for prediction in predictions:
            confidence = float(prediction["confidence"])
            if confidence >= confidence_threshold:
                label = prediction["label"]
                prediction_dict[label] = prediction_dict[label] + 1
        
        ## Calculate TP, FP and FN
        for event in metric_dict.keys():
            number_of_labels = labels_dict[event]
            number_of_predicions = prediction_dict[event]

            if number_of_predicions >= number_of_labels:
                true_positive = number_of_labels
                false_positive = number_of_predicions - number_of_labels
                false_negative = 0
            else:
                true_positive = number_of_predicions
                false_positive = 0
                false_negative = number_of_labels - number_of_predicions
            
            metric_dict[event]["True positive"] = metric_dict[event]["True positive"] + true_positive
            metric_dict[event]["False positive"] = metric_dict[event]["False positive"] + false_positive
            metric_dict[event]["False negative"] = metric_dict[event]["False negative"] + false_negative

    
    total_tp = 0
    total_fp = 0
    total_fn = 0

    for event_name in metric_dict.keys():
        total_tp += metric_dict[event_name]["True positive"]
        total_fp += metric_dict[event_name]["False positive"]
        total_fn += metric_dict[event_name]["False negative"]
    
    metric_dict["Total"] = defaultdict(lambda: 0)
    metric_dict["Total"]["True positive"] = total_tp
    metric_dict["Total"]["False positive"] = total_fp
    metric_dict["Total"]["False negative"] = total_fn
    
    ## Calculate metrics
    for event_name in metric_dict.keys():
        true_positive = metric_dict[event_name]["True positive"]
        false_positive = metric_dict[event_name]["False positive"]
        false_negative = metric_dict[event_name]["False negative"]
        
        if (true_positive + false_positive) != 0:
            precision = true_positive / (true_positive + false_positive)
            metric_dict[event_name]["Precision"] = precision
            recall = true_positive / (true_positive + false_negative)
            metric_dict[event_name]["Recall"] = recall 
            metric_dict[event_name]["F1_score"] = 2 * ((precision * recall) / (precision + recall))

    pretty_print_metrics(metric_dict)
    return metric_dict

def evaluate_over_confidence_intervals(SoccerNet_path, Predictions_path, n_intervals=10, prediction_file="results_spotting.json", split="test"):
    confidence_levels = [i/n_intervals for i in range(0, n_intervals)]
    list_games = getListGames(split=split)

    """

    [
        "goal": {
            "0.0": {
                {
                    "True positive": 3,
                    "False positive": 3,
                    "False negative": 5,
                },
            },
            "0.1": {
                {
                    "True positive": 3,
                    "False positive": 3,
                    "False negative": 5,
                },
            },
            ...
        },
        "corner": {
            "0.0": {
                {
                    "True positive": 3,
                    "False positive": 3,
                    "False negative": 5,
                },
            },
            "0.1": {
                {
                    "True positive": 3,
                    "False positive": 3,
                    "False negative": 5,
                },
            },
            ...
        },
        ...
    ]
    """

    # Setup dict
    metric_dict = dict()
    for event_name in EVENT_DICTIONARY_V2.keys():
        confidence_dict = dict()
        for confidence_threshold in confidence_levels:
            confidence_dict[str(confidence_threshold)] = defaultdict(lambda: 0)
        metric_dict[event_name] = confidence_dict

    for game in tqdm(list_games):
        

        """
        PREDICTION AND LABEL DICT
            [
            "goal": {
                "0.0": 12,
                "0.1": 20,
                ...
            },
            "corner": {
                "0.0": 22,
                "0.1": 30,
                ...
            },
            ...
        ]
        """

        prediction_dict = dict()
        for event_name in EVENT_DICTIONARY_V2.keys():
            # dict with predicion per class per confidence threshold
            prediction_dict[event_name] = defaultdict(lambda: 0)

        # dict with labels per class
        labels_dict = defaultdict(lambda: 0)

        ## Count labels per class
        label_files = "Labels-v2.json"
        labels = json.load(open(os.path.join(SoccerNet_path, game, label_files)))
        annotations = labels["annotations"]
        for annotation in annotations:
            label = annotation["label"]
            labels_dict[label] = labels_dict[label] + 1

        ## Count predicions per class
        predictions_file_dict = json.load(open(os.path.join(Predictions_path, game, prediction_file)))        
        predictions = predictions_file_dict["predictions"]
        for prediction in predictions:
            label = prediction["label"]
            confidence = float(prediction["confidence"])
            for confidence_threshold in confidence_levels:
                if confidence >= confidence_threshold:
                    prediction_dict[label][str(confidence_threshold)] = prediction_dict[label][str(confidence_threshold)] + 1
        

        ## Calculate TP, FP and FN
        for event in metric_dict.keys():
            number_of_labels = labels_dict[event]
            for confidence_threshold in confidence_levels:
                number_of_predicions = prediction_dict[event][str(confidence_threshold)]

                if number_of_predicions >= number_of_labels:
                    true_positive = number_of_labels
                    false_positive = number_of_predicions - number_of_labels
                    false_negative = 0
                else:
                    true_positive = number_of_predicions
                    false_positive = 0
                    false_negative = number_of_labels - number_of_predicions
                
                metric_dict[event][str(confidence_threshold)]["True positive"] = metric_dict[event][str(confidence_threshold)]["True positive"] + true_positive
                metric_dict[event][str(confidence_threshold)]["False positive"] = metric_dict[event][str(confidence_threshold)]["False positive"] + false_positive
                metric_dict[event][str(confidence_threshold)]["False negative"] = metric_dict[event][str(confidence_threshold)]["False negative"] + false_negative

    
    total_tp = np.zeros(n_intervals)
    total_fp = np.zeros(n_intervals)
    total_fn = np.zeros(n_intervals)

    for event_name in metric_dict.keys():
        for i, confidence_threshold in enumerate(confidence_levels):
            total_tp[i] = total_tp[i] + metric_dict[event_name][str(confidence_threshold)]["True positive"]
            total_fp[i] = total_fp[i] + metric_dict[event_name][str(confidence_threshold)]["False positive"]
            total_fn[i] = total_fn[i] + metric_dict[event_name][str(confidence_threshold)]["False negative"]
    
    precisions_array = np.full(n_intervals, np.nan)
    recalls_array = np.full(n_intervals, np.nan)
    f1_score_array = np.full(n_intervals, np.nan)
    ## Calculate metrics
    for i, confidence_threshold in enumerate(confidence_levels):

        true_positive = total_tp[i]
        false_positive = total_fp[i]
        false_negative = total_fn[i]
        
        if (true_positive + false_positive) != 0:
            precision = true_positive / (true_positive + false_positive)
            recall = true_positive / (true_positive + false_negative)
            f1_score = 2 * ((precision * recall) / (precision + recall))
            precisions_array[i] = precision
            recalls_array[i] = recall
            f1_score_array[i] = f1_score

    return precisions_array, recalls_array, f1_score_array

def pretty_print_metrics(metric_dict):
    for event_name in metric_dict.keys():
        print(f"\n{event_name}\n---------------")
        for key, value in metric_dict[event_name].items():
            print(f"    {key}: {round(value, 4)}")
        