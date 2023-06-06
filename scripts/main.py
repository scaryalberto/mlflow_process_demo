# main.py
import mlflow
import click
import os

@click.command()
@click.option("--param_1", type=str)
@click.option("--param_2", type=str)
def workflow(param_1, param_2):
  with mlflow.start_run() as active_run:

    print("ENTRATO00000000000000000000000")
    print(param_1, param_2)


    print("Launching 'data_prep'")
    download_run = mlflow.run(".", "data_prep", parameters={"param_1": param_1, "param_2":param_2})
    download_run = mlflow.tracking.MlflowClient().get_run(download_run.run_id)

    print("ULTIMATO")

if __name__ == '__main__':
  workflow()