from evaluate import evaluate_predictions

def create_file(src):
    file = open(src)
    line = file.readline()
    model_name = line.replace("INFO:root:Model name: ", "").strip()
    print(model_name)
    file.readline()
    
    ## Total
    line = file.readline()
    total = float(line.split(":")[3].strip()) * 100

    line = file.readline()
    total_per_class = [float(x) * 100 for x in line.split(":")[3].strip().replace("[", "").replace("]", "").split(", ")]

    ## Visible only
    line = file.readline()
    visible = float(line.split(":")[3].strip()) * 100

    line = file.readline()
    visible_per_class = [float(x) * 100 for x in line.split(":")[3].strip().replace("[", "").replace("]", "").split(", ")]
    
    ## Unshown only
    line = file.readline()
    unshown = float(line.split(":")[3].strip()) * 100

    line = file.readline()
    unshown_per_class = [float(x) * 100 for x in line.split(":")[3].strip().replace("[", "").replace("]", "").split(", ")]

    start_list = [total, visible, unshown]

    total_list = start_list + total_per_class
    visible_list = start_list + visible_per_class
    unshown_list = start_list + unshown_per_class
    
    # print(str(total_list).replace("[", "").replace("]", ""))
    # print(str(visible_list).replace("[", "").replace("]", ""))
    # print(str(unshown_list).replace("[", "").replace("]", ""))

    new_filename = src.replace(".log", "_extra.log")
    new_file = open(new_filename, "w")
    new_file.write(str(total_list).replace("[", "").replace("]", ""))
    new_file.write(str(total_list).replace("[", "").replace("]", ""))
    new_file.write(str(total_list).replace("[", "").replace("]", ""))
    
    new_file.close()
    file.close()




if __name__ == '__main__':

    evaluate_predictions("/global/D1/projects/soccer_clipping/haakhern_brynjabm_thesis/original_features",
                        "/global/D1/projects/soccer_clipping/haakhern_brynjabm_thesis/models/NetVLAD++/outputs_test",
                        "test_model_1")

    # print("start")
    # create_file("/global/D1/projects/soccer_clipping/haakhern_brynjabm_thesis/brynjard/ContextAwareActionSpotting/experiments/experiment_5/ex_5.2-25secs_timeframe.log")
    # print("end")