import os
import pandas as pd
from prediction import PredictionPipeline

if __name__=="__main__":
    # print("Hello, world!")
    path_to_model = os.path.join(os.getcwd(), "model.keras")
    pipeline = PredictionPipeline(path_to_model)

    df_comments = pd.read_csv("comments.csv")

    df_comments['prediction'] = df_comments['message'].apply(lambda x: "Negative" if x == 0 else "Positive" , pipeline.predict)