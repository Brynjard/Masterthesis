from re import A
import sys
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from alternative_evaluation import create_scores_dict
from SoccerNet.Evaluation.utils import EVENT_DICTIONARY_V2

def plot_scores_per_class(metric, result_array, filename, colors):
    
    confidence_levels = np.linspace(0, 1-1/(len(result_array[0])), len(result_array[0]))
    
    plt.title(f"{metric} at confidence thresholds")

    plt.xlabel("Confidence threshold")
    plt.ylabel(metric)
    ax = plt.gca()
    ax.set_prop_cycle(color=colors)

    for i, array in enumerate(result_array):
        plt.plot(confidence_levels, array, label=list(EVENT_DICTIONARY_V2.keys())[i])
    
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

    if len(args) < 3:
        print(f"2 command line arguments expected, {len(args) - 1} found")
        exit()
    
    ## Need 7 extra colors
    list_of_extra_colors = ["indigo", "gold", "navy", "lime", "darkred", "darkslategray", "salmon"]
    list_of_extra_colors_hex = [mcolors.to_hex(c) for c in list_of_extra_colors]
    colors = list(mcolors.TABLEAU_COLORS.values()) + list_of_extra_colors_hex
    
    soccer_net_path = args[1]
    predictions_folder = args[2]

    scores_dict = create_scores_dict(SoccerNet_path=soccer_net_path, Predictions_path=predictions_folder)

    ## Create a list of lists with values for the different scores
    list_of_lists_precision = list()
    list_of_lists_recall = list()
    list_of_lists_f1score = list()
    for event_name in EVENT_DICTIONARY_V2.keys():
        list_of_lists_precision.append(scores_dict["precision"][event_name])
        list_of_lists_recall.append(scores_dict["recall"][event_name])
        list_of_lists_f1score.append(scores_dict["f1_score"][event_name])

    plot_scores_per_class("Precision", list_of_lists_precision, "precision_per_class", colors)
    plot_scores_per_class("Recall", list_of_lists_recall, "recall_per_class", colors)
    plot_scores_per_class("F1 Score", list_of_lists_f1score, "f1score_per_class", colors)