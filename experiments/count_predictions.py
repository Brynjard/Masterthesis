import sys
import datafusion_utils as fusion_utils

if __name__ == '__main__':

    args = sys.argv

    if len(args) < 2:
        print(f"1 command line arguments expected, {len(args) - 1} found")
        exit()


    current = 0
    past = 0
    future = 0

    src = args[1]

    pred_dict = fusion_utils.create_prediction_dict(src)
    

    for game_url in pred_dict.keys():
        url = pred_dict[game_url]["url"]
        
        predictions = pred_dict[game_url]["predictions"]
        for p in predictions:
            if p["model"] == "past":
                past += 1
            elif p["model"] == "current":
                current += 1
            elif p["model"] == "future":
                future += 1
    print("Past", past)
    print("Current", current)
    print("Future", future)