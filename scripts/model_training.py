
import click
import sys
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.svm import SVR
import pickle
import numpy as np
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import r2_score
from urllib.parse import urlparse
import pickle
import click


@click.command()
@click.option("--kernel", type=str)
@click.option("--c", type=int)
@click.option("--model_path", type=str)
@click.option("--val_dataset_path", type=str)
def train_model(kernel, c, model_path, val_dataset_path):
    if kernel is None:
        kernel='linear'


    X_train = pd.read_csv(f'{val_dataset_path}X_train.csv', index_col=0)
    y_train = pd.read_csv(f'{val_dataset_path}y_train.csv', index_col=0)
    y_train = y_train['VALORE PRIORITA\'']
    
    # kernel = 'linear'
    # C = float(sys.argv[2]) if len(sys.argv) > 2 else 5
    # parameters = {'kernel':kernel, 'C': C}
    with mlflow.start_run():
        svr = SVR(C=c, kernel=kernel)
        
        svr.fit(X_train, y_train)
        #salva svr come pickle e chiamalo da lì per inference
    
    print("Uploading output: %s" % svr)
    #mlflow.log_artifacts(svr, "svr")
    #mlflow.log_artifact(parameters, 'parameters')
    with open(model_path, 'wb') as f:
        pickle.dump(svr, f)

if __name__ == '__main__':
    train_model()
    