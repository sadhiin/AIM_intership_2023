import os
import argparse
import logging
import pandas as pd
from prediction import PredictionPipeline

if __name__=="__main__":
    args = argparse.ArgumentParser(usage="To run the prediciton form scraped comments run 'python main.py --model model.keras --comments comments.csv --output output.csv'")
    args.add_argument("--model", help="Path to the model")
    args.add_argument("--comments", help="Path to the comments")
    args.add_argument("--output", help="Path to the output file")

    parser = args.parse_args()
    logging.basicConfig(level=logging.INFO)
    try:
        logging.info("Loading the model from {}".format(parser.model)
                     )
        pipeline = PredictionPipeline(parser.model)
        logging.info("Loading the comments {}".format(parser.comments))
        df_comments = pd.read_csv(parser.comments, encoding='utf-8')

        logging.info("Predicting the sentiment of the comments")
        df_comments['prediction'] = df_comments['message'].apply(lambda x: "Negative" if x == 0 else "Positive" , pipeline.predict)
        logging.info("Saving the output to {}".format(parser.output))
        df_comments.to_csv(parser.output, encoding='utf-8', index=False)

    except Exception as e:
        logging.error(e)
        logging.error("Please provide the correct paths to the model, comments and output file")
        exit(1)