import pandas as pd 

DATASET = "./data/datasets/wla/municity.raw.csv"

df = pd.read_csv(DATASET)

df = df.dropna()

df.to_csv("./data/datasets/wla/municity.csv")

print(df)