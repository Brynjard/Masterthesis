from re import A
import sys
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from alternative_evaluation import create_scores_dict, evaluate_individual_confidence_thresholds, pretty_print_metrics
from table_creation_statistics_usecase import create_table_statistics
from event_list import EVENT_LIST

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
    
    confidence_dict = dict()

    for event_name in EVENT_LIST:
        print(f"{event_name}: ", end="")
        [print(round(x, 2), end=" ") for x in scores_dict["f1_score"][event_name]]
        print("")
        # print(scores_dict["f1_score"][event_name])
        max_score = max(scores_dict["f1_score"][event_name])
        result_tuple = np.where(scores_dict["f1_score"][event_name] == max_score)
        index = result_tuple[0][0]
        confidence_dict[event_name] = index / 10
    # print(confidence_dict)
    confidence_dict["Yellow->red card"] = 0.1

    for k, v in confidence_dict.items():
        print(F"{k}: {v}")

    score_dict = evaluate_individual_confidence_thresholds(SoccerNet_path=soccer_net_path, Predictions_path=predictions_folder, confidence_thresholds=confidence_dict)

    pretty_print_metrics(score_dict)

    