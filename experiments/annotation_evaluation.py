import os
import glob
import json
import zipfile
import numpy as np
from collections import defaultdict

from SoccerNet.utils import getListGames
from SoccerNet.Evaluation.utils import LoadJsonFromZip, EVENT_DICTIONARY_V2, INVERSE_EVENT_DICTIONARY_V2
from SoccerNet.Evaluation.utils import EVENT_DICTIONARY_V1, INVERSE_EVENT_DICTIONARY_V1
from tqdm import tqdm

from event_list import EVENT_DICT, EVENT_DICT_INVERSE
from metric_types_dicts import METRIC_TYPE_DICT_INVERSE

def evaluate(SoccerNet_path, Predictions_path, delta, prediction_file="results_spotting.json", split="test"):
    # evaluate the prediction with respect to some ground truth
    # Params:
    #   - SoccerNet_path: path for labels (folder or zipped file)
    #   - Predictions_path: path for predictions (folder or zipped file)
    #   - prediction_file: name of the predicted files - if set to None, try to infer it
    #   - split: split to evaluate from ["test", "challenge"]
    #   - frame_rate: frame rate to evalaute from [2]
    # Return:
    #   - details mAP
    framerate = 2
    list_games = getListGames(split=split)
    targets_numpy = list()
    detections_numpy = list()
    closests_numpy = list()

    version = 2
    label_files = "Labels-v2.json"
    num_classes = 17


    total_annotations = 0
    for game in tqdm(list_games):

        # Load labels
        if zipfile.is_zipfile(SoccerNet_path):
            labels = LoadJsonFromZip(SoccerNet_path, os.path.join(game, label_files))
        else:
            labels = json.load(open(os.path.join(SoccerNet_path, game, label_files)))
        # convert labels to vector
        label_half_1, label_half_2 = label2vector(
            labels, num_classes=num_classes, version=version)
        # print(version)
        

        # if game == "europe_uefa-champions-league/2016-2017/2017-03-08 - 22-45 Barcelona 6 - 1 Paris SG":
        #     print(f"Goals first half: {len(np.where(label_half_1[:,2] != 0)[0])}")
        #     print(f"Goals second half: {len(np.where(label_half_2[:,2] != 0)[0])}")

        #     n_goals = sum([1 if annotation['label'] == 'Goal' else 0 for annotation in labels["annotations"]])
        #     print(f"Goal from list: {n_goals}")

        # n_game_label_annotations = len(np.where(label_half_1[:,2] != 0)[0]) + len(np.where(label_half_2[:,2] != 0)[0])
        # # print(n_game_label_annotations)
        # # n_goals = len([annotation['label'] == 'Goal' for annotation in labels["annotations"]])
        # n_goals = sum([1 if annotation['label'] == 'Goal' else 0 for annotation in labels["annotations"]])
        
        # if n_goals != n_game_label_annotations:
        #     print(f"Game: {game} \nNumber of goals from label2vector: {n_game_label_annotations} \nNumber of goals from annotation list: {n_goals}")



        # infer name of the prediction_file
        if prediction_file == None:
            if zipfile.is_zipfile(Predictions_path):
                with zipfile.ZipFile(Predictions_path, "r") as z:
                    for filename in z.namelist():
                        #       print(filename)
                        if filename.endswith(".json"):
                            prediction_file = os.path.basename(filename)
                            break
            else:
                for filename in glob.glob(os.path.join(Predictions_path,"*/*/*/*.json")):
                    prediction_file = os.path.basename(filename)
                    # print(prediction_file)
                    break

        # Load predictions
        if zipfile.is_zipfile(Predictions_path):
            predictions = LoadJsonFromZip(Predictions_path, os.path.join(game, prediction_file))
        else:
            predictions = json.load(open(os.path.join(Predictions_path, game, prediction_file)))
        # convert predictions to vector
        predictions_half_1, predictions_half_2 = predictions2vector(predictions, num_classes=num_classes, version=version)

        targets_numpy.append(label_half_1)
        targets_numpy.append(label_half_2)
        detections_numpy.append(predictions_half_1)
        detections_numpy.append(predictions_half_2)

        ## Filter on confidence?
        ## count number of predictions per class
        ## count number of labels per class
        ## Calculate TP
        ## Add these numbers to global 


        closest_numpy = np.zeros(label_half_1.shape)-1 #10800 x 17 with -1 values.
        #Get the closest action index
        for c in np.arange(label_half_1.shape[-1]): #for each class (17 times..)
            indexes = np.where(label_half_1[:,c] != 0)[0].tolist() #index of Every frame in first half that is annotated with this class.. 
            if len(indexes) == 0 : #If we have no annotations in first half..
                continue
            indexes.insert(0,-indexes[0])
            indexes.append(2*closest_numpy.shape[0])
            for i in np.arange(len(indexes)-2)+1: #For all frames annotated with c..
                start = max(0,(indexes[i-1]+indexes[i])//2)
                stop = min(closest_numpy.shape[0], (indexes[i]+indexes[i+1])//2)
                closest_numpy[start:stop,c] = label_half_1[indexes[i],c]
        closests_numpy.append(closest_numpy)

        closest_numpy = np.zeros(label_half_2.shape)-1
        for c in np.arange(label_half_2.shape[-1]):
            indexes = np.where(label_half_2[:,c] != 0)[0].tolist()
            if len(indexes) == 0 :
                continue
            indexes.insert(0,-indexes[0])
            indexes.append(2*closest_numpy.shape[0])
            for i in np.arange(len(indexes)-2)+1:
                start = max(0,(indexes[i-1]+indexes[i])//2)
                stop = min(closest_numpy.shape[0], (indexes[i]+indexes[i+1])//2)
                closest_numpy[start:stop,c] = label_half_2[indexes[i],c]
        closests_numpy.append(closest_numpy)

    

    return compute_precision_recall_curve(targets_numpy, closests_numpy, detections_numpy, delta)




def label2vector(labels, num_classes=17, framerate=2, version=2):


    vector_size = 90*60*framerate

    label_half1 = np.zeros((vector_size, num_classes))
    label_half2 = np.zeros((vector_size, num_classes))

    for annotation in labels["annotations"]:

        time = annotation["gameTime"]
        event = annotation["label"]

        half = int(time[0])

        minutes = int(time[-5:-3])
        seconds = int(time[-2::])
        frame = framerate * ( seconds + 60 * minutes ) 

        if version == 2:
            if event not in EVENT_DICTIONARY_V2:
                continue
            label = EVENT_DICTIONARY_V2[event]
        elif version == 1:
            # print(event)
            # label = EVENT_DICTIONARY_V1[event]
            if "card" in event: label = 0
            elif "subs" in event: label = 1
            elif "soccer" in event: label = 2
            else: 
                # print(event)
                continue
        # print(event, label, half)

        value = 1
        if "visibility" in annotation.keys():
            if annotation["visibility"] == "not shown":
                value = -1

        if half == 1:
            frame = min(frame, vector_size-1)
            label_half1[frame][label] = value

        if half == 2:
            frame = min(frame, vector_size-1)
            label_half2[frame][label] = value

    return label_half1, label_half2

def predictions2vector(predictions, num_classes=17, version=2, framerate=2):


    vector_size = 90*60*framerate

    prediction_half1 = np.zeros((vector_size, num_classes))-1
    prediction_half2 = np.zeros((vector_size, num_classes))-1

    for annotation in predictions["predictions"]:

        time = int(annotation["position"])
        event = annotation["label"]

        half = int(annotation["half"])

        frame = int(framerate * ( time/1000 ))

        if version == 2:
            if event not in EVENT_DICTIONARY_V2:
                continue
            label = EVENT_DICTIONARY_V2[event]
        elif version == 1:
            label = EVENT_DICTIONARY_V1[event]
            # print(label)
            # EVENT_DICTIONARY_V1[l]
            # if "card" in event: label=0
            # elif "subs" in event: label=1
            # elif "soccer" in event: label=2
            # else: continue

        value = annotation["confidence"]

        if half == 1:
            frame = min(frame, vector_size-1)
            prediction_half1[frame][label] = value

        if half == 2:
            frame = min(frame, vector_size-1)
            prediction_half2[frame][label] = value

    return prediction_half1, prediction_half2


import numpy as np
from tqdm import tqdm
import time
np.seterr(divide='ignore', invalid='ignore')

class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

def NMS(detections, delta):
    
    # Array to put the results of the NMS
    detections_tmp = np.copy(detections)
    detections_NMS = np.zeros(detections.shape)-1

    # Loop over all classes
    for i in np.arange(detections.shape[-1]):
        # Stopping condition
        while(np.max(detections_tmp[:,i]) >= 0):

            # Get the max remaining index and value
            max_value = np.max(detections_tmp[:,i])
            max_index = np.argmax(detections_tmp[:,i])

            detections_NMS[max_index,i] = max_value

            detections_tmp[int(np.maximum(-(delta/2)+max_index,0)): int(np.minimum(max_index+int(delta/2), detections.shape[0])) ,i] = -1

    return detections_NMS

def compute_class_scores(target, closest, detection, delta):

    # Retrieving the important variables
    gt_indexes = np.where(target != 0)[0]
    gt_indexes_visible = np.where(target > 0)[0]
    gt_indexes_unshown = np.where(target < 0)[0]
    pred_indexes = np.where(detection >= 0)[0]
    pred_scores = detection[pred_indexes]

    # Array to save the results, each is [pred_scor,{1 or 0}]
    game_detections = np.zeros((len(pred_indexes),3))
    game_detections[:,0] = np.copy(pred_scores)
    game_detections[:,2] = np.copy(closest[pred_indexes])


    remove_indexes = list()

    for gt_index in gt_indexes:

        max_score = -1
        max_index = None
        game_index = 0
        selected_game_index = 0

        for pred_index, pred_score in zip(pred_indexes, pred_scores):

            if pred_index < gt_index - delta:
                game_index += 1
                continue
            if pred_index > gt_index + delta:
                break

            if abs(pred_index-gt_index) <= delta/2 and pred_score > max_score and pred_index not in remove_indexes:
                max_score = pred_score
                max_index = pred_index
                selected_game_index = game_index
            game_index += 1

        if max_index is not None:
            game_detections[selected_game_index,1]=1
            remove_indexes.append(max_index)

    return game_detections, len(gt_indexes_visible), len(gt_indexes_unshown)



def compute_precision_recall_curve(targets, closests, detections, delta):
    
    # Store the number of classes
    num_classes = targets[0].shape[-1]

    # 200 confidence thresholds between [0,1]
    # thresholds = np.linspace(0,1,200) #array of evenly spaced values between 0 - 1, (200 elements)
    thresholds = np.linspace(0, 1-(1/200), 200)

    # Store the precision and recall points
    precision = list()
    precision_visible = list()
    precision_unshown = list()

    recall = list()
    recall_visible = list()
    recall_unshown = list()

    f1_score = list()
    f1_score_visible = list()
    f1_score_unshown = list()

    true_positive = list()
    true_positive_visible = list()
    true_positive_unshown = list()
    false_positive = list()
    false_positive_visible = list()
    false_positive_unshown = list()
    false_negative = list()
    false_negative_visible = list()
    false_negative_unshown = list()


    # Apply Non-Maxima Suppression if required
    start = time.time()

    # Precompute the predictions scores and their correspondence {TP, FP} for each class
    for c in np.arange(num_classes):
        total_detections =  np.zeros((1, 3)) #[[0. 0. 0.]]
        total_detections[0,0] = -1
        n_gt_labels_visible = 0
        n_gt_labels_unshown = 0
        
        # Get the confidence scores and their corresponding TP or FP characteristics for each game
        for target, closest, detection in zip(targets, closests, detections):
            tmp_detections, tmp_n_gt_labels_visible, tmp_n_gt_labels_unshown = compute_class_scores(target[:,c], closest[:,c], detection[:,c], delta)
            total_detections = np.append(total_detections,tmp_detections,axis=0)
            n_gt_labels_visible = n_gt_labels_visible + tmp_n_gt_labels_visible
            n_gt_labels_unshown = n_gt_labels_unshown + tmp_n_gt_labels_unshown

        precision.append(list())
        precision_visible.append(list())
        precision_unshown.append(list())
        
        recall.append(list())
        recall_visible.append(list())
        recall_unshown.append(list())

        f1_score.append(list())
        f1_score_visible.append(list())
        f1_score_unshown.append(list())

        ###
        true_positive.append(list())
        true_positive_visible.append(list())
        true_positive_unshown.append(list())
        false_positive.append(list())
        false_positive_visible.append(list())
        false_positive_unshown.append(list())
        false_negative.append(list())
        false_negative_visible.append(list())
        false_negative_unshown.append(list())

        # Get only the visible or unshown actions
        total_detections_visible = np.copy(total_detections)
        total_detections_unshown = np.copy(total_detections)
        total_detections_visible[np.where(total_detections_visible[:,2] <= 0.5)[0],0] = -1
        total_detections_unshown[np.where(total_detections_unshown[:,2] >= -0.5)[0],0] = -1

        # Get the precision and recall for each confidence threshold
        for threshold in thresholds:
            pred_indexes = np.where(total_detections[:,0]>=threshold)[0]
            pred_indexes_visible = np.where(total_detections_visible[:,0]>=threshold)[0]
            pred_indexes_unshown = np.where(total_detections_unshown[:,0]>=threshold)[0]
            
            TP = np.sum(total_detections[pred_indexes,1])
            TP_visible = np.sum(total_detections[pred_indexes_visible,1])
            TP_unshown = np.sum(total_detections[pred_indexes_unshown,1])

            FP = len(pred_indexes) - TP
            FP_visible = len(pred_indexes_visible) - TP_visible
            FP_unshown = len(pred_indexes_unshown) - TP_unshown

            FN = (n_gt_labels_visible + n_gt_labels_unshown) - TP
            FN_visible = n_gt_labels_visible - TP_visible
            FN_unshown = n_gt_labels_unshown - TP_unshown

            p = np.nan_to_num(TP/len(pred_indexes))
            p_visible = np.nan_to_num(TP_visible/len(pred_indexes_visible))
            p_unshown = np.nan_to_num(TP_unshown/len(pred_indexes_unshown))
            
            r = np.nan_to_num(TP/(n_gt_labels_visible + n_gt_labels_unshown))
            r_visible = np.nan_to_num(TP_visible/n_gt_labels_visible)
            r_unshown = np.nan_to_num(TP_unshown/n_gt_labels_unshown)

            f1 = np.nan_to_num(2*(p*r)/(p+r))
            f1_visible = np.nan_to_num(2*(p_visible*r_visible)/(p_visible+r_visible))
            f1_unshown = np.nan_to_num(2*(p_unshown*r_unshown)/(p_unshown+r_unshown))


            precision[-1].append(p)
            precision_visible[-1].append(p_visible)
            precision_unshown[-1].append(p_unshown)

            recall[-1].append(r)
            recall_visible[-1].append(r_visible)
            recall_unshown[-1].append(r_unshown)

            f1_score[-1].append(f1)
            f1_score_visible[-1].append(f1_visible)
            f1_score_unshown[-1].append(f1_unshown)

            true_positive[-1].append(TP)
            true_positive_visible[-1].append(TP_visible)
            true_positive_unshown[-1].append(TP_unshown)
            false_positive[-1].append(FP)
            false_positive_visible[-1].append(FP_visible)
            false_positive_unshown[-1].append(FP_unshown)
            false_negative[-1].append(FN)
            false_negative_visible[-1].append(FN_visible)
            false_negative_unshown[-1].append(FN_unshown)


    precision = np.array(precision).transpose()
    precision_visible = np.array(precision_visible).transpose()
    precision_unshown = np.array(precision_unshown).transpose()

    recall = np.array(recall).transpose()
    recall_visible = np.array(recall_visible).transpose()
    recall_unshown = np.array(recall_unshown).transpose()

    f1_score = np.array(f1_score).transpose()
    f1_score_visible = np.array(f1_score_visible).transpose()
    f1_score_unshown = np.array(f1_score_unshown).transpose()

    true_positive = np.array(true_positive).transpose()
    true_positive_visible = np.array(true_positive_visible).transpose()
    true_positive_unshown = np.array(true_positive_unshown).transpose()
    false_positive = np.array(false_positive).transpose()
    false_positive_visible = np.array(false_positive_visible).transpose()
    false_positive_unshown = np.array(false_positive_unshown).transpose()
    false_negative = np.array(false_negative).transpose()
    false_negative_visible = np.array(false_negative_visible).transpose()
    false_negative_unshown = np.array(false_negative_unshown).transpose()


    return precision, precision_visible, precision_unshown, \
            recall, recall_visible, recall_unshown, \
            f1_score, f1_score_visible, f1_score_unshown, \
            true_positive, true_positive_visible, true_positive_unshown, \
            false_positive, false_positive_visible, false_positive_unshown, \
            false_negative, false_negative_visible, false_negative_unshown

def get_value_from_confidence_level(array, confidence_threshold):
    index =  confidence_threshold / 0.005
    return array[index:]

def create_scores_dict_from_numpy_array(data_array, n_confidence_thresholds):
    scores_dict = defaultdict(lambda: "")

    confidence_thresholds = np.linspace(0, 1 - (1 / n_confidence_thresholds), n_confidence_thresholds)
    indices = [round(e / 0.005) for e in confidence_thresholds]

    ## for precision, recall, f1_score and all, visible and unshown
    for i in range(9):
        metric_with_n_confidence_levels = data_array[i,indices,:]
        metric_dict = defaultdict(lambda: "")
        for j in range(17):
            classwise_scores = metric_with_n_confidence_levels[:,j]
            metric_dict[EVENT_DICT_INVERSE[j]] = classwise_scores
        scores_dict[METRIC_TYPE_DICT_INVERSE[i]] = metric_dict

    return scores_dict


if __name__ == '__main__':
    delta = 30

    precision, precision_visible, precision_unshown, \
    recall, recall_visible, recall_unshown, \
    f1_score, f1_score_visible, f1_score_unshown, \
    true_positive, true_positive_visible, true_positive_unshown, \
    false_positive, false_positive_visible, false_positive_unshown, \
    false_negative, false_negative_visible, false_negative_unshown = evaluate("/global/D1/projects/soccer_clipping/haakhern_brynjabm_thesis/original_features", "/global/D1/projects/soccer_clipping/haakhern_brynjabm_thesis/haakon/ContextAwareActionSpotting/experiments/experiment_5/fusion_out", delta=delta, prediction_file="results_spotting.json", split="test",)
    
    # print((np.arange(12)*5 + 5)*2)
    print("------------------------------")
    tp_new = np.add(true_positive_visible[0], true_positive_unshown[0])
    print(true_positive[0]) 
    print(tp_new)
    print(np.sum(tp_new))

    print("------------------------------")
    fp_new = np.add(false_positive_visible[0], false_positive_unshown[0])
    print(false_positive[0]) 
    print(fp_new)
    print(np.sum(fp_new))
    print("------------------------------")
    fn_new = np.add(false_negative_visible[0], false_negative_unshown[0])
    print(false_negative[0]) 
    print(fn_new)
    print(np.sum(fn_new))
    print("--------------  LABELS PER CLASS ----------------")
    labels_per_class = np.add(true_positive[0], false_negative[0])
    print(labels_per_class)
    print(f"Sum: {np.sum(labels_per_class)}")



    # print(EVENT_DICTIONARY_V2)
    # print(true_positive[140].shape)
    # newArr = np.add(true_positive[0], false_negative[0])
    # print(newArr)
    # print(f"Total preds: {np.sum(newArr)}")
    # print(true_positive[140])
    # print(precision[140])
    
    
