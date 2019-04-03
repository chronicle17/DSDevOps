import os
import azureml
from azureml.core import Experiment
from azureml.core import Workspace

def getExperiment():
    ws = Workspace.from_config()
    script_folder = "."
    experiment_name = 'devops-ai'
    exp = Experiment(workspace=ws, name=experiment_name)
    print(exp.name, exp.workspace.name, sep='\n')
    return exp

if __name__ == "__main__":
    exp = getExperiment()