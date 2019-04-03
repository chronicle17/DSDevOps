import pickle
from azureml.core import Workspace
from azureml.core.run import Run
import os
from sklearn.datasets import load_diabetes
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import numpy as np
import json
import subprocess
from typing import Tuple, List

# run_history_name = 'devops-ai'
#os.makedirs('./outputs', exist_ok=True)
# #ws.get_details()
# Start recording results to AML
#run = Run.start_logging(workspace = ws, history_name = run_history_name)
run = Run.get_submitted_run()


X, y = load_diabetes(return_X_y = True)
columns = ['age', 'gender', 'bmi', 'bp', 's1', 's2', 's3', 's4', 's5', 's6']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
data = {
    "train":{"X": X_train, "y": y_train},        
    "test":{"X": X_test, "y": y_test}
}

print('Running train.py')

# Randomly pic alpha
alphas = np.arange(0.0, 1.0, 0.05)
alpha=alphas[np.random.choice(alphas.shape[0], 1, replace=False)][0]
print(alpha)
run.log('alpha', alpha)
reg = Ridge(alpha = alpha)
reg.fit(data['train']['X'], data['train']['y'])
preds = reg.predict(data['test']['X'])
run.log('mse', mean_squared_error(preds, data['test']['y']))


# Save model as part of the run history
model_name = "sklearn_regression_model.pkl"
# model_name = "."

with open(model_name, "wb") as file:
    joblib.dump(value = reg, filename = model_name)

# upload the model file explicitly into artifacts 
run.upload_file(name = './outputs/'+ model_name, path_or_stream = model_name)
print('Uploaded the model {} to experiment {}'.format(model_name, run.experiment.name))
dirpath = os.getcwd()
print(dirpath)


# register the model
# run.log_model(file_name = model_name)
# print('Registered the model {} to run history {}'.format(model_name, run.history.name))



print('Following files are uploaded ')
print(run.get_file_names())
run.complete()