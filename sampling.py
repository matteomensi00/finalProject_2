#!/usr/bin/python3

if __name__== "__main__":

    import pandas as pd
    data=pd.read_csv("train.csv") #tramite kaggle
    sample = data.copy().sample(n=1000, random_state=42)
    sample.to_csv("trainsampled.csv", index=False)