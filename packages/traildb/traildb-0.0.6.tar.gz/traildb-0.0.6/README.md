# Trail db

A small demo library to save mlflow run data to a mongodb.
Prerequisite is using mlflow to track experiments.

# Installation

pip install traildb

# Get started

from traildb import DB_import

# Instantiate a DB_import object
db_imp = DB_import(URI, database_name)

# Call the add_db method after the mlflow run (not within the run)
db_imp.MLflow_to_db(mlflow.get_run(run_id=run.info.run_id))
