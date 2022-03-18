import sys
import os
import numpy as np
import matplotlib.pyplot as plt

from SoccerNet.Evaluation.utils import EVENT_DICTIONARY_V2, INVERSE_EVENT_DICTIONARY_V2

from event_list import EVENT_LIST, EVENT_DICT, EVENT_DICT_INVERSE
from metric_types_dicts import METRIC_TYPE_DICT, METRIC_TYPE_DICT_INVERSE
from annotation_evaluation import create_scores_dict_from_numpy_array
from table_creation_statistics_usecase import create_table_statistics


def create_plot(metric, result_array, baseline_array, filename):
    
    confidence_levels = np.linspace(0, 1-1/(len(result_array)), len(result_array))
    
    plt.title(f"{metric} at confidence thresholds")

    plt.xlabel("Confidence threshold")
    plt.ylabel(metric)

    plt.plot(confidence_levels, result_array, label="Our model", color="red")
    plt.plot(confidence_levels, baseline_array, label="Baseline", color="darkviolet")

    plt.xticks(np.linspace(0, 1.0, 11))
    plt.yticks(np.linspace(0, 1.0, 11))
    plt.legend()
    plt.grid()

    plt.savefig(f"{filename}.png")
    plt.clf()

def get_total_metric_over_confidence_levels(metrics_array, metric, n_confidence_thresholds):
    ## Get total precision per confidence.
    ## We want an array with shape (n_confidence_thresholds)

    confidence_thresholds = np.linspace(0, 1-(1/n_confidence_thresholds), n_confidence_thresholds)
    indices = [round(e / 0.005) for e in confidence_thresholds]
    
    ## Extract the value at the n confidence levels we want, from the metrics array
    ## New shape is (n_confidence_thresholds, 17)
    metric_with_n_confidence_levels = metrics_array[METRIC_TYPE_DICT[metric],indices,:]
    
    # Average over the 17 classes
    total_metric_over_thresholds = np.average(metric_with_n_confidence_levels, 1)
    return total_metric_over_thresholds

def get_total_precision_over_confidence_levels(metrics_array, n_confidence_thresholds, visibility=""):
    if visibility != "": visibility = "_" + visibility

    confidence_thresholds = np.linspace(0, 1 - (1 / n_confidence_thresholds), n_confidence_thresholds)
    indices = [round(e / 0.005) for e in confidence_thresholds]

    # Get TP
    true_positive_with_n_confidence_levels = metrics_array[METRIC_TYPE_DICT["true_positive" + visibility],indices,:]
    total_true_positives = np.sum(true_positive_with_n_confidence_levels, 1)

    # Get FP
    false_positive_with_n_confidence_levels = metrics_array[METRIC_TYPE_DICT["false_positive" + visibility],indices,:]
    total_false_positives = np.sum(false_positive_with_n_confidence_levels, 1)

    precision_array = np.zeros((n_confidence_thresholds))

    for i in range(len(precision_array)):
        precision_array[i] = total_true_positives[i] / (total_true_positives[i] + total_false_positives[i])
    return precision_array

def get_total_recall_over_confidence_levels(metrics_array, n_confidence_thresholds, visibility=""):
    if visibility != "": visibility = "_" + visibility

    confidence_thresholds = np.linspace(0, 1 - (1 / n_confidence_thresholds), n_confidence_thresholds)
    indices = [round(e / 0.005) for e in confidence_thresholds]

    # Get TP
    true_positive_with_n_confidence_levels = metrics_array[METRIC_TYPE_DICT["true_positive" + visibility],indices,:]
    total_true_positives = np.sum(true_positive_with_n_confidence_levels, 1)

    # Get FN
    false_negative_with_n_confidence_levels = metrics_array[METRIC_TYPE_DICT["false_negative" + visibility],indices,:]
    total_false_negatives = np.sum(false_negative_with_n_confidence_levels, 1)

    recall_array = np.zeros((n_confidence_thresholds))

    for i in range(len(recall_array)):
        recall_array[i] = total_true_positives[i] / (total_true_positives[i] + total_false_negatives[i])
    return recall_array

def get_total_f1_score_over_confidence_levels(metrics_array, n_confidence_thresholds, visibility=""):
    if visibility != "": visibility = "_" + visibility
    
    confidence_thresholds = np.linspace(0, 1 - (1 / n_confidence_thresholds), n_confidence_thresholds)
    indices = [round(e / 0.005) for e in confidence_thresholds]

    # Get TP
    true_positive_with_n_confidence_levels = metrics_array[METRIC_TYPE_DICT["true_positive" + visibility],indices,:]
    total_true_positives = np.sum(true_positive_with_n_confidence_levels, 1)
    
    # Get FP
    false_positive_with_n_confidence_levels = metrics_array[METRIC_TYPE_DICT["false_positive" + visibility],indices,:]
    total_false_positives = np.sum(false_positive_with_n_confidence_levels, 1)

    # Get FN
    false_negative_with_n_confidence_levels = metrics_array[METRIC_TYPE_DICT["false_negative" + visibility],indices,:]
    total_false_negatives = np.sum(false_negative_with_n_confidence_levels, 1)

    f1_array = np.zeros((n_confidence_thresholds))

    for i in range(len(f1_array)):
        precision = total_true_positives[i] / (total_true_positives[i] + total_false_positives[i])
        recall = total_true_positives[i] / (total_true_positives[i] + total_false_negatives[i])
        ## Check for 0?
        f1_array[i] = 2 * (precision * recall) / (precision + recall)
    return f1_array

if __name__ == '__main__':
    args = sys.argv

    if len(args) < 2:
        print(f"2 command line arguments expected, {len(args) - 1} found")
        exit()
    delta = int(args[1])
    if not os.path.isdir(f'lcg_{delta}'):
        os.mkdir(f'lcg_{delta}')

    filepath_our_model = f'/global/D1/projects/soccer_clipping/haakhern_brynjabm_thesis/haakon/ContextAwareActionSpotting/experiments/use_case_live_game_commentary/metrics_our_model_delta_{delta}.npy'
    filepath_baseline = f'/global/D1/projects/soccer_clipping/haakhern_brynjabm_thesis/haakon/ContextAwareActionSpotting/experiments/use_case_live_game_commentary/metrics_baseline_delta_{delta}.npy'
    n_confidence_thresholds = 20
    metrics_array_our_model = np.load(filepath_our_model)
    metrics_array_baseline = np.load(filepath_baseline)
    
    scores_dict = create_scores_dict_from_numpy_array(data_array=metrics_array_our_model, n_confidence_thresholds=10)
    
    ## ALL
    ## PRECISION
    total_precision_over_thresholds_our_model = get_total_precision_over_confidence_levels(metrics_array_our_model, n_confidence_thresholds)
    
    total_precision_over_thresholds_baseline = get_total_precision_over_confidence_levels(metrics_array_baseline, n_confidence_thresholds)

    create_plot("Total precision", total_precision_over_thresholds_our_model, total_precision_over_thresholds_baseline, f"lcg_{delta}/lgc_total_precision_{delta}")

    ## RECALL
    total_recall_over_thresholds_our_model = get_total_recall_over_confidence_levels(metrics_array_our_model, n_confidence_thresholds)
    
    total_recall_over_thresholds_baseline = get_total_recall_over_confidence_levels(metrics_array_baseline, n_confidence_thresholds)

    create_plot("Total recall", total_recall_over_thresholds_our_model, total_recall_over_thresholds_baseline, f"lcg_{delta}/lgc_total_recall_{delta}")

    ## f1 score
    total_f1_score_over_thresholds_our_model = get_total_f1_score_over_confidence_levels(metrics_array_our_model, n_confidence_thresholds)
    
    total_f1_score_over_thresholds_baseline = get_total_f1_score_over_confidence_levels(metrics_array_baseline, n_confidence_thresholds)

    create_plot("Total F1 Score", total_f1_score_over_thresholds_our_model, total_f1_score_over_thresholds_baseline, f"lcg_{delta}/lgc_total_f1score_{delta}")

    ## VISIBLE
    ## PRECISION
    total_precision_over_thresholds_our_model = get_total_precision_over_confidence_levels(metrics_array_our_model, n_confidence_thresholds, "visible")
    
    total_precision_over_thresholds_baseline = get_total_precision_over_confidence_levels(metrics_array_baseline, n_confidence_thresholds, "visible")

    create_plot("Total precision", total_precision_over_thresholds_our_model, total_precision_over_thresholds_baseline, f"lcg_{delta}/lgc_total_precision_visible_{delta}")

    ## RECALL
    total_recall_over_thresholds_our_model = get_total_recall_over_confidence_levels(metrics_array_our_model, n_confidence_thresholds, "visible")
    
    total_recall_over_thresholds_baseline = get_total_recall_over_confidence_levels(metrics_array_baseline, n_confidence_thresholds, "visible")

    create_plot("Total recall", total_recall_over_thresholds_our_model, total_recall_over_thresholds_baseline, f"lcg_{delta}/lgc_total_recall_visible_{delta}")


    ## f1 score
    total_f1_score_over_thresholds_our_model = get_total_f1_score_over_confidence_levels(metrics_array_our_model, n_confidence_thresholds, "visible")
    
    total_f1_score_over_thresholds_baseline = get_total_f1_score_over_confidence_levels(metrics_array_baseline, n_confidence_thresholds, "visible")

    create_plot("Total F1 Score visible", total_f1_score_over_thresholds_our_model, total_f1_score_over_thresholds_baseline, f"lcg_{delta}/lgc_total_f1score_visible_{delta}")
    
    ## UNSHOWN
    ## PRECISION
    total_precision_over_thresholds_our_model = get_total_precision_over_confidence_levels(metrics_array_our_model, n_confidence_thresholds, "unshown")
    
    total_precision_over_thresholds_baseline = get_total_precision_over_confidence_levels(metrics_array_baseline, n_confidence_thresholds, "unshown")
    

    create_plot("Total precision", total_precision_over_thresholds_our_model, total_precision_over_thresholds_baseline, f"lcg_{delta}/lgc_total_precision_unshown_{delta}")

    ## RECALL
    total_recall_over_thresholds_our_model = get_total_recall_over_confidence_levels(metrics_array_our_model, n_confidence_thresholds, "unshown")
    
    total_recall_over_thresholds_baseline = get_total_recall_over_confidence_levels(metrics_array_baseline, n_confidence_thresholds, "unshown")

    create_plot("Total recall", total_recall_over_thresholds_our_model, total_recall_over_thresholds_baseline, f"lcg_{delta}/lgc_total_recall_unshown_{delta}")

    ## f1 score
    total_f1_score_over_thresholds_our_model = get_total_f1_score_over_confidence_levels(metrics_array_our_model, n_confidence_thresholds, "unshown")
    
    total_f1_score_over_thresholds_baseline = get_total_f1_score_over_confidence_levels(metrics_array_baseline, n_confidence_thresholds, "unshown")

    create_plot("Total F1 Score", total_f1_score_over_thresholds_our_model, total_f1_score_over_thresholds_baseline, f"lcg_{delta}/lgc_total_f1score_unshown_{delta}")
