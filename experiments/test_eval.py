import sys
from alternative_evaluation import evaluate_no_delta


if __name__ == '__main__':
    args = sys.argv

    if len(args) < 4:
        print(f"3 command line arguments expected, {len(args) - 1} found")
        exit()

    model_name = args[3]
    soccer_net_path = args[1]
    split = "test"
    predictions_folder = args[2]
    output_results = f"results_spotting_{split}.zip"


    evaluate_no_delta(SoccerNet_path=soccer_net_path,
                            Predictions_path=predictions_folder)