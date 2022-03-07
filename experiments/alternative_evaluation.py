from cProfile import label
import os
from turtle import pos
import numpy as np

from SoccerNet.utils import getListGames
from SoccerNet.Evaluation.utils import LoadJsonFromZip, EVENT_DICTIONARY_V2, INVERSE_EVENT_DICTIONARY_V2
from SoccerNet.Evaluation.utils import EVENT_DICTIONARY_V1, INVERSE_EVENT_DICTIONARY_V1
from SoccerNet.Evaluation.ActionSpotting import label2vector, predictions2vector, compute_class_scores, compute_mAP, delta_curve, average_mAP
import glob
import json
import zipfile
from tqdm import tqdm
from collections import defaultdict

def evaluate_no_delta(SoccerNet_path, Predictions_path, prediction_file="results_spotting.json", split="test", version=2):
    list_games = getListGames(split=split)
    ## dict with TP, FP and FN per class

    ## classes
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
    events = ['Penalty',
                'Kick-off',
                'Goal',
                'Substitution',
                'Offside',
                'Shots on target',
                'Shots off target',
                'Clearance',
                'Ball out of play',
                'Throw-in',
                'Foul',
                'Indirect free-kick',
                'Direct free-kick',
                'Corner',
                'Yellow card',
                'Red card',
                'Yellow->red card']
    # Setup dict
    metric_dict = dict()
    for event_name in EVENT_DICTIONARY_V2.keys():
        metric_dict[event_name] = defaultdict(lambda: 0)
        # {"True positive": 0, "False positive": 0, "False negative": 0}

    for game in tqdm(list_games):
        
        # dict with predicion per class
        prediction_dict = defaultdict(lambda: 0)
        # dict with labels per class
        labels_dict = defaultdict(lambda: 0)

        # Load labels
        if version==2:
            label_files = "Labels-v2.json"
            num_classes = 17
        if version==1:
            label_files = "Labels.json"
            num_classes = 3
        if zipfile.is_zipfile(SoccerNet_path):
            labels = LoadJsonFromZip(SoccerNet_path, os.path.join(game, label_files))
        else:
            labels = json.load(open(os.path.join(SoccerNet_path, game, label_files)))
        # convert labels to vector
        label_half_1, label_half_2 = label2vector(
            labels, num_classes=num_classes, version=version)


        # print("----------------------------------------")
        # print(labels["UrlLocal"])

        annotations = labels["annotations"]
        for annotation in annotations:
            label = annotation["label"]
            labels_dict[label] = labels_dict[label] + 1
        
        # print(labels_dict)
        # print("----------------------------------------")

        predictions_file_dict = json.load(open(os.path.join(Predictions_path, game, prediction_file)))
        
        predictions = predictions_file_dict["predictions"]
        for prediction in predictions:
            confidence = float(prediction["confidence"])
            if confidence >= 0.8:
                label = prediction["label"]
                prediction_dict[label] = prediction_dict[label] + 1


        
        ## Calculate FN 
        for event in metric_dict.keys():
            number_of_labels = labels_dict[event]
            number_of_predicions = prediction_dict[event]
            
            ## Calculate TP
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

def pretty_print_metrics(metric_dict):
    for event_name in metric_dict.keys():
        print(f"\n{event_name}\n---------------")
        for key, value in metric_dict[event_name].items():
            print(f"    {key}: {round(value, 4)}")
        