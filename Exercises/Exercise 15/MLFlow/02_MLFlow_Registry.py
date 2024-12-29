import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import platform
import psutil
import socket

# Ensure your MLflow server is running on the specified URI
mlflow.set_tracking_uri("http://127.0.0.1:5000")  # Replace with your server URI
mlflow.set_experiment("digits_randomforest")

# Integrate MLflow tracking into the training script
def train_and_log_model():
    # Load the Digits dataset
    data = load_digits()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=42
    )

    # Model parameters
    n_estimators = 50  # Number of trees in the forest
    max_depth = 5  # Maximum depth of the tree

    # Train RandomForestClassifier
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions
    predictions = model.predict(X_test)

    # Calculate metrics
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, average="weighted")
    recall = recall_score(y_test, predictions, average="weighted")
    f1 = f1_score(y_test, predictions, average="weighted")

    # Capture system information
    system_info = {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "platform-release": platform.release(),
        "cpu-count": psutil.cpu_count(logical=True),
        "memory": psutil.virtual_memory().total
    }

    # Start MLflow run
    with mlflow.start_run() as run:
        # Log parameters
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)

        # Log metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)

        # Log the model
        mlflow.sklearn.log_model(model, "model")

        # Register the model in the MLflow model registry
        model_uri = f"runs:/{run.info.run_id}/model"
        registered_model_name = "digits_random_forest_classifier"
        #mlflow.register_model(model_uri=model_uri, name=registered_model_name)

        # Transition the model to the "Staging" stage
        client = MlflowClient()
        client.transition_model_version_stage(
            name=registered_model_name,
            version= 2,
            stage="Archived"
        )

        # Log system information
        for key, value in system_info.items():
            mlflow.log_param(key, value)

    print("Model training, logging, and registration complete.")
    print(f"Accuracy: {accuracy:.2f}, Precision: {precision:.2f}, Recall: {recall:.2f}, F1 Score: {f1:.2f}")

if __name__ == "__main__":
    train_and_log_model()
