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
   """
   Funzione che rielabora i dataset in formato csv passati.

   Args:
       param_1 (str): percorso del dataset
       param_2 (str): percorso del dataset

   """

   print("eeeeeeeeeeeeeeeeeee")
   print(param_1)


   #TODO: devo scaricare il dataset da un link?
   url = "http://www.example.com/file.csv"
   #df = pd.read_csv(url)
   #print(df.head())

   if param_1.endswith('.csv'):
      df = pd.read_csv(param_1)
      #"C:\\Users\\alsg\\PycharmProjects\\mlflow_mio_per_github\\dataset\\markers_quartieri.csv"
      print("letto csv")

   else:
      raise "Non è un csv"


if __name__ == '__main__':
   data_prep()
    