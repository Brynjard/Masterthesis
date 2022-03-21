import sys
import os
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from alternative_evaluation import create_scores_dict
from table_creation_statistics_usecase import create_table_statistics
from event_list import EVENT_LIST
from annotation_evaluation import create_scores_dict_from_numpy_array

def plot_scores_per_class(metric, result_array, filename, colors):
    
    confidence_levels = np.linspace(0, 1-1/(len(result_array[0])), len(result_array[0]))
    
    plt.title(f"{metric} at confidence thresholds")

    plt.xlabel("Confidence threshold")
    plt.ylabel(metric)
    ax = plt.gca()
    ax.set_prop_cycle(color=colors)

    for i, array in enumerate(result_array):
        plt.plot(confidence_levels, array, label=EVENT_LIST[i])
    
    fig = plt.gcf()
    fig.set_size_inches(10, 5)
    plt.xticks(np.linspace(0, 1.0, 11))
    plt.yticks(np.linspace(0, 1.0, 11))
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid()
    plt.savefig(fname=f"{filename}.png", bbox_inches="tight")
    plt.clf()

if __name__ == '__main__':

    args = sys.argv

    if len(args) < 2:
        print(f"2 command line arguments expected, {len(args) - 1} found")
        exit()
    delta = int(args[1])
    if not os.path.isdir(f'lcg_{delta}'):
        os.mkdir(f'lcg_{delta}')
    
    ## Need 7 extra colors
    list_of_extra_colors = ["indigo", "gold", "navy", "lime", "darkred", "darkslategray", "salmon"]
    list_of_extra_colors_hex = [mcolors.to_hex(c) for c in list_of_extra_colors]
    colors = list(mcolors.TABLEAU_COLORS.values()) + list_of_extra_colors_hex
    
    
    filepath_our_model = f'/global/D1/projects/soccer_clipping/haakhern_brynjabm_thesis/haakon/ContextAwareActionSpotting/experiments/use_case_live_game_commentary/metrics_our_model_delta_{delta}.npy'
    filepath_baseline = f'/global/D1/projects/soccer_clipping/haakhern_brynjabm_thesis/haakon/ContextAwareActionSpotting/experiments/use_case_live_game_commentary/metrics_baseline_delta_{delta}.npy'
    n_confidence_thresholds = 20
    metrics_array_our_model = np.load(filepath_our_model)
    metrics_array_baseline = np.load(filepath_baseline)
    model = "baseline"
    scores_dict = create_scores_dict_from_numpy_array(data_array=metrics_array_baseline, n_confidence_thresholds=10)

    ## Create a list of lists with values for the different scores
    list_of_lists_precision = list()
    list_of_lists_precision_visible = list()
    list_of_lists_precision_unshown = list()
    list_of_lists_recall = list()
    list_of_lists_recall_visible = list()
    list_of_lists_recall_unshown = list()
    list_of_lists_f1_score = list()
    list_of_lists_f1_score_visible = list()
    list_of_lists_f1_score_unshown = list()

    for event_name in EVENT_LIST:
        list_of_lists_precision.append(scores_dict["precision"][event_name])
        list_of_lists_precision_visible.append(scores_dict["precision_visible"][event_name])
        list_of_lists_precision_unshown.append(scores_dict["precision_unshown"][event_name])
        list_of_lists_recall.append(scores_dict["recall"][event_name])
        list_of_lists_recall_visible.append(scores_dict["recall_visible"][event_name])
        list_of_lists_recall_unshown.append(scores_dict["recall_unshown"][event_name])
        list_of_lists_f1_score.append(scores_dict["f1_score"][event_name])
        list_of_lists_f1_score_visible.append(scores_dict["f1_score_visible"][event_name])
        list_of_lists_f1_score_unshown.append(scores_dict["f1_score_unshown"][event_name])

    plot_scores_per_class("Precision", list_of_lists_precision, f'lcg_{delta}/lgc_precision_per_class_{delta}_{model}', colors)
    plot_scores_per_class("Precision visible", list_of_lists_precision_visible, f'lcg_{delta}/lgc_precision_visible_per_class_{delta}_{model}', colors)
    plot_scores_per_class("Precision unshown", list_of_lists_precision_unshown, f'lcg_{delta}/lgc_precision_unshown_per_class_{delta}_{model}', colors)
    plot_scores_per_class("Recall", list_of_lists_recall, f'lcg_{delta}/lgc_recall_per_class_{delta}_{model}', colors)
    plot_scores_per_class("Recall visible", list_of_lists_recall_visible, f'lcg_{delta}/lgc_recall_visible_per_class_{delta}_{model}', colors)
    plot_scores_per_class("Recall unshown", list_of_lists_recall_unshown, f'lcg_{delta}/lgc_recall_unshown_per_class_{delta}_{model}', colors)
    plot_scores_per_class("F1 Score", list_of_lists_f1_score, f'lcg_{delta}/lgc_f1_score_per_class_{delta}_{model}', colors)
    plot_scores_per_class("F1 Score visible", list_of_lists_f1_score_visible, f'lcg_{delta}/lgc_f1_score_visible_per_class_{delta}_{model}', colors)
    plot_scores_per_class("F1 Score unshown", list_of_lists_f1_score_unshown, f'lcg_{delta}/lgc_f1_score_unshown_per_class_{delta}_{model}', colors)
    
    file = open(f'lcg_{delta}/lgc_class_tables_{delta}_{model}.txt', 'w')

    
    
    file.write("\n---------------------- PRECISION ----------------------\n")
    precision_string = create_table_statistics("precision", scores_dict)
    file.write(precision_string)
    file.write("\n---------------------- PRECISION VISIBLE ----------------------\n")
    precision_string = create_table_statistics("precision_visible", scores_dict)
    file.write(precision_string)
    file.write("\n---------------------- PRECISION UNSHOWN ----------------------\n")
    precision_string = create_table_statistics("precision_unshown", scores_dict)
    file.write(precision_string)

    file.write("\n---------------------- RECALL ----------------------")
    recall_string = create_table_statistics("recall", scores_dict)
    file.write(recall_string)
    file.write("\n---------------------- RECALL VISIBLE ----------------------")
    recall_string = create_table_statistics("recall_visible", scores_dict)
    file.write(recall_string)
    file.write("\n---------------------- RECALL UNSHOWN ----------------------")
    recall_string = create_table_statistics("recall_unshown", scores_dict)
    file.write(recall_string)

    
    file.write("\n---------------------- F1 SCORE ----------------------\n")
    f1_score_string = create_table_statistics("f1_score", scores_dict)
    file.write(f1_score_string)
    file.write("\n---------------------- F1 SCORE VISIBLE ----------------------\n")
    f1_score_string = create_table_statistics("f1_score_visible", scores_dict)
    file.write(f1_score_string)
    file.write("\n---------------------- F1 SCORE UNSHOWN ----------------------\n")
    f1_score_string = create_table_statistics("f1_score_unshown", scores_dict)
    file.write(f1_score_string)


    file.close()