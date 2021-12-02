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

    plt.rcParams["figure.figsize"] = [30,5]
    plt.title("Half: {} class: {}".format(half, class_name))
    #plotting ground-truth:
    x_vals = [int(l["position"]) for l in labels if l["label"] == class_name and int(l["gameTime"][0]) == half]
    y_vals = np.ones(len(x_vals))
    for x, y in zip(x_vals, y_vals):
        x_points = [x, x]
        y_points = [0, 1]
        plt.plot(x_points, y_points, "b")
    
    #Plotting predictions:
    x_vals = [int(p["position"]) for p in preds if p["label"] == class_name and int(p["gameTime"][0]) == half] 
    y_vals = [float(p["confidence"]) for p in preds if p["label"] == class_name and int(p["gameTime"][0]) == half]
    for x, y in zip(x_vals, y_vals):
        x_points = [x, x]
        y_points = [0, y]
        plt.plot(x_points, y_points, "r--")

    ticks = []
    for i in range(0, 3000000, 500000):
        ticks.append(int(i))
    labels = [int(i / 1000) for i in ticks]
    plt.xticks(ticks, labels)
    plt.axis([0, 3000000, 0, 1])
    plt.tight_layout()
    plt.xlabel("Time(s)")
    plt.ylabel("Confidence")
    plt.legend(["ground-truth", "prediction"], loc="upper left")
    plt.savefig("{}_{}.png".format(half, class_name))
    

if __name__ == '__main__':
    args = sys.argv
    labels_src = args[1] #source of label-files
    pred_src = args[2] #source of pred-files
    current_class = args[3] #which class to evaluate?

    preds_dictionary = fu.create_prediction_dict(pred_src)
    labels_dictionary = lu.create_label_dict_relative_urlkey(labels_src, "Labels-v2.json")

    preds = preds_dictionary["england_epl/2014-2015/2015-05-17 - 18-00 Manchester United 1 - 1 Arsenal/results_spotting.json"]["predictions"]
    labels = labels_dictionary["england_epl/2014-2015/2015-05-17 - 18-00 Manchester United 1 - 1 Arsenal/Labels-v2.json"]["annotations"]
    
    create_plot_half(preds, labels, 1, current_class)
    create_plot_half(preds, labels, 2, current_class)
    




