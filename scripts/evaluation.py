
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


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mape = mean_absolute_percentage_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mape, r2



@click.command()
@click.option("--model_path", type=str)
@click.option("--validate_dataset_path", type=str)
def eval_model(model_path, validate_dataset_path):    
    svr = pickle.load(open(model_path, 'rb'))
    #validate_dataset_path
    X_test = pd.read_csv(f'{validate_dataset_path}X_test.csv', index_col=0)
    y_test = pd.read_csv(f'{validate_dataset_path}y_test.csv', index_col=0)
    y_test = y_test['VALORE PRIORITA\'']
    svr_y_pred = svr.predict(X_test)
    (rmse, mape, r2) = eval_metrics(y_test, svr_y_pred)
    
    
    
    # print(f"SVR model (kernel={kernel}, C={C}):")
    # print("  RMSE: %s" % rmse)
    # print("  MAPE: %s" % mape)
    # print("  R2: %s" % r2)
    
    #mlflow.log_param("kernel", kernel)
    #mlflow.log_param("C", C)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)
    mlflow.log_metric("mape", mape)
    
    tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        
if __name__ == '__main__':
    eval_model()
    