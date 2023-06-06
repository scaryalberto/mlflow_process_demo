import os 
import json
import pandas as pd
from sklearn.model_selection import train_test_split
import mlflow
import click

@click.command()
@click.option("--param_1", type=str)
@click.option("--param_2", type=str)
def data_prep(param_1, param_2):

   print("eeeeeeeeeeeeeeeeeee")
   print(param_1)

   url = "http://www.example.com/file.csv"
   #df = pd.read_csv(url)
   #print(df.head())

   #TODO: devo scaricare il dataset da un link?
   import pdb
   #pdb.set_trace()
   df = pd.read_csv(param_1)
   #"C:\\Users\\alsg\\PycharmProjects\\mlflow_mio_per_github\\dataset\\markers_quartieri.csv"

   print("letto csv")


if __name__ == '__main__':
   data_prep()
    