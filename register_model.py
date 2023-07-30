### Register the model on MLflow Model Registry
import sys
import mlflow
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType



mlflow.set_tracking_uri("http://127.0.0.1:5000")

def run_register_model(top_n: int):
    '''Register the best model from the experiment'''
    client = MlflowClient()

    # Retrieve the top_n model runs and log the models
    experiment = client.get_experiment_by_name("Klopps-Liverpool-experiment")
    client.search_runs(
        experiment_ids=experiment.experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=top_n,
        order_by=["metrics.rmse ASC"]
    )

    # Select the model with the lowest test RMSE
    experiment = client.get_experiment_by_name("Klopps-Liverpool-experiment")
    best_run = client.search_runs(
        experiment_ids=experiment.experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=1,
        order_by=["metrics.test_rmse ASC"]
    )[0]

    # Register the best model
    run_id = best_run.info.run_id
    model_uri = f"runs:/{run_id}/model"
    model_name = "best_decision_tree_model"
    mlflow.register_model(model_uri, model_name)
    return print(f"Registered model name: {model_name} and URI: {model_uri}")


if __name__ == "__main__":
    TOP_N = int(sys.argv[1])
    run_register_model(top_n = TOP_N)
