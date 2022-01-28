"""
Compares a model to the labels of a given game, and visualizes this
with a graph. 
"""
import matplotlib.pyplot as plt
import datafusion_utils as fu
import modify_labels_utils as lu
import sys
import numpy as np

def create_subplot_half(preds, labels, half, class_name, subplot, legend_labels):

    subplot.set_title("{}".format(class_name))
    #plotting ground-truth:
    x_vals = [(int(l["position"]), l["visibility"]) for l in labels if l["label"] == class_name and int(l["gameTime"][0]) == half]
    y_vals = np.ones(len(x_vals))

    for x, y in zip(x_vals, y_vals):
        x_points = [x[0], x[0]]
        y_points = [0, 1]
        if x[1] == "not shown":
            if "not_shown" not in legend_labels:
                subplot.plot(x_points, y_points, "g", label="not_shown")
                legend_labels.append("not_shown")
            else:
                subplot.plot(x_points, y_points, "g")
        else:
            if "shown" not in legend_labels:
                subplot.plot(x_points, y_points, "b", label="shown")
                legend_labels.append("shown")
            else:
                subplot.plot(x_points, y_points, "b")
    
    #Plotting predictions:
    x_vals = [(int(p["position"]), p["model"]) for p in preds if p["label"] == class_name and int(p["gameTime"][0]) == half] 
    y_vals = [(float(p["confidence"]), p["model"]) for p in preds if p["label"] == class_name and int(p["gameTime"][0]) == half]
    for x, y in zip(x_vals, y_vals):
        x_points = [x[0], x[0]]
        y_points = [0, y[0]]

        if x[1] == "future":
            if "future_pred" not in legend_labels:
                subplot.plot(x_points, y_points, "c--", label="future_pred")
                legend_labels.append("future_pred")  
            else:  
                subplot.plot(x_points, y_points, "c--")
        elif x[1] == "past":
            if "past_pred" not in legend_labels:
                subplot.plot(x_points, y_points, "m--", label="past_pred")
                legend_labels.append("past_pred")
            else:
                subplot.plot(x_points, y_points, "m--")
            
        else:
            if "current_pred" not in legend_labels:
                subplot.plot(x_points, y_points, "r--", label="current_pred")
                legend_labels.append("current_pred")
            else:
                subplot.plot(x_points, y_points, "r--")
        
    ticks = []
    for i in range(-60000, 3000000, 60000):
        ticks.append(int(i))

    labels = [fu.convert_position_to_gamestring(int(i)) for i in ticks]
    subplot.set_xlim([0, 3000000])
    subplot.set_ylim([0, 1])
    subplot.set_xticks(ticks)
    subplot.set_xticklabels(labels)
    plt.xlabel("Time(m)")
    plt.ylabel("Confidence")
    subplot.set(xlabel="Time(m)", ylabel="Confidence")
    #concating labels for legend:
    
    
def create_visualization(classes, half, preds, labels, filename, game_url):
    legend_labels = []
    fig, axes = plt.subplots(len(classes), figsize=(50, 50))
    fig.suptitle(game_url)
    if len(classes) > 1:
        for i, c in enumerate(classes):
            create_subplot_half(preds, labels, half, c, axes[i], legend_labels)
    else:
        create_subplot_half(preds, labels, half, classes[0], axes, legend_labels)
    fig.tight_layout()
    fig.legend()
    fig.savefig("{}.png".format(filename))
    fig.clf()

if __name__ == '__main__':
    args = sys.argv
    labels_src = args[1] #source of label-files
    pred_src = args[2] #source of pred-files
    filename = args[3]
    #classes = args[4:]  #which class to evaluate?
    #classes = [ARGUMENT_MAPPER[c] for c in classes]
    classes = ["Goal", "Kick-off", "Shots off target", "Shots on target", "Ball out of play", "Throw-in", "Clearance", "Corner", "Foul", "Indirect free-kick", "Direct free-kick", "Penalty", "Yellow card", "Red card","Yellow->red card", "Offside", "Substitution"]

    preds_dictionary = fu.create_prediction_dict(pred_src)
    labels_dictionary = lu.create_label_dict_relative_urlkey(labels_src, "Labels-v2.json")

    preds = preds_dictionary["england_epl/2016-2017/2017-01-21 - 15-30 Liverpool 2 - 3 Swansea/results_spotting.json"]["predictions"]
    labels = labels_dictionary["england_epl/2016-2017/2017-01-21 - 15-30 Liverpool 2 - 3 Swansea/Labels-v2.json"]["annotations"]
    game_url = "england_epl/2016-2017/2017-01-21 - 15-30 Liverpool 2 - 3 Swansea"
    #create_plot_half(preds, labels, 2, current_class)
    """legend_labels = []
    fig, axes = plt.subplots(5, figsize=(30, 8))
    fig.suptitle("Title for whole figure..")
    create_subplot_half(preds, labels, 2, "Goal", axes[0], legend_labels)
    create_subplot_half(preds, labels, 2, "Kick-off", axes[1], legend_labels)
    create_subplot_half(preds, labels, 2, "Throw-in", axes[2], legend_labels)"""
    create_visualization(classes, 1, preds, labels, "{}_half1".format(filename), game_url)
    create_visualization(classes, 2, preds, labels, "{}_half2".format(filename), game_url)

    




