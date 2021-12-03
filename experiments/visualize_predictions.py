"""
Compares a model to the labels of a given game, and visualizes this
with a graph. 
"""
import matplotlib.pyplot as plt
import datafusion_utils as fu
import modify_labels_utils as lu
import sys
import numpy as np

def create_plot_half(preds, labels, half, class_name):

    not_shown_counter = 0
    shown_counter = 0
    past_counter = 0
    current_counter = 0
    future_counter = 0

    plt.rcParams["figure.figsize"] = [30,5]
    plt.title("Half: {} class: {}".format(half, class_name))
    #plotting ground-truth:
    x_vals = [(int(l["position"]), l["visibility"]) for l in labels if l["label"] == class_name and int(l["gameTime"][0]) == half]
    y_vals = np.ones(len(x_vals))
    not_shown = []
    shown = []
    for x, y in zip(x_vals, y_vals):
        x_points = [x[0], x[0]]
        y_points = [0, 1]
        if x[1] == "not shown":
            if not_shown_counter == 0:
                plt.plot(x_points, y_points, "g", label="not_shown")
            else:
                plt.plot(x_points, y_points, "g")
            not_shown_counter += 1
        else:
            if shown_counter == 0:
                plt.plot(x_points, y_points, "b", label="shown")
            else:
                plt.plot(x_points, y_points, "b")
            shown_counter += 1
    
    #Plotting predictions:
    x_vals = [(int(p["position"]), p["model"]) for p in preds if p["label"] == class_name and int(p["gameTime"][0]) == half] 
    y_vals = [(float(p["confidence"]), p["model"]) for p in preds if p["label"] == class_name and int(p["gameTime"][0]) == half]
    for x, y in zip(x_vals, y_vals):
        x_points = [x[0], x[0]]
        y_points = [0, y[0]]

        if x[1] == "future":
            if future_counter == 0:
                plt.plot(x_points, y_points, "c--", label="future_pred")  
            else:  
                plt.plot(x_points, y_points, "c--")
            future_counter += 1
        elif x[1] == "past":
            if past_counter == 0:
                plt.plot(x_points, y_points, "m--", label="past_pred")
            else:
                plt.plot(x_points, y_points, "m--")
            past_counter += 1
            
        else:
            if current_counter == 0:
                current_pred = plt.plot(x_points, y_points, "r--", label="current_pred")
            else:
                current_pred = plt.plot(x_points, y_points, "r--")
            current_counter += 1
        

    ticks = []
    for i in range(0, 3000000, 500000):
        ticks.append(int(i))
    labels = [int(i / 1000) for i in ticks]
    plt.xticks(ticks, labels)
    plt.axis([0, 3000000, 0, 1])
    plt.tight_layout()
    plt.xlabel("Time(s)")
    plt.ylabel("Confidence")
    #concating labels for legend:
    
    plt.legend()
    plt.savefig("{}_{}.png".format(half, class_name))
    plt.clf()
    
    

if __name__ == '__main__':
    args = sys.argv
    labels_src = args[1] #source of label-files
    pred_src = args[2] #source of pred-files
    current_class = " ".join(args[3:])  #which class to evaluate?

    preds_dictionary = fu.create_prediction_dict(pred_src)
    labels_dictionary = lu.create_label_dict_relative_urlkey(labels_src, "Labels-v2.json")

    preds = preds_dictionary["england_epl/2014-2015/2015-05-17 - 18-00 Manchester United 1 - 1 Arsenal/results_spotting.json"]["predictions"]
    labels = labels_dictionary["england_epl/2014-2015/2015-05-17 - 18-00 Manchester United 1 - 1 Arsenal/Labels-v2.json"]["annotations"]
    
    create_plot_half(preds, labels, 1, current_class)
    create_plot_half(preds, labels, 2, current_class)
    




