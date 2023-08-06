import pandas as pd
from src.antm import ANTM

#load data
df=pd.read_parquet("./data/dblpFullSchema_2000_2020_extract_big_data_1K.parquet")
df=df[["abstract","year"]].rename(columns={"abstract":"content","year":"time"}).dropna().reset_index()

#choosing the windows size and overlapping length for time frames
window_size=3
overlap=1

#initialize model
model=ANTM(df,overlap,window_size,mode="data2vec",num_words=10,path="./saved_data")

#learn the model and save it
model.fit(save=True)
