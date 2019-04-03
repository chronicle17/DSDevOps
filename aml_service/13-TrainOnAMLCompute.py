from azureml.core import Workspace
from azureml.core import Experiment
import os
import shutil
from azureml.core.runconfig import RunConfiguration
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import DEFAULT_CPU_IMAGE

ws = Workspace.from_config(path='./aml_config/config.json')
print(ws.name)

experiment_name = 'train-on-amlcompute'
experiment = Experiment(workspace = ws, name = experiment_name)

project_folder = './train-on-amlcompute'
os.makedirs(project_folder, exist_ok=True)
shutil.copy('/code/training/train.py', project_folder)

# create a new runconfig object
run_config = RunConfiguration()

# signal that you want to use AmlCompute to execute script.
run_config.target = "amlcompute"

# AmlCompute will be created in the same region as workspace
# Set vm size for AmlCompute
run_config.amlcompute.vm_size = 'STANDARD_D2_V2'

# enable Docker 
run_config.environment.docker.enabled = True

# set Docker base image to the default CPU-based image
run_config.environment.docker.base_image = DEFAULT_CPU_IMAGE

# use conda_dependencies.yml to create a conda environment in the Docker image for execution
run_config.environment.python.user_managed_dependencies = False

# auto-prepare the Docker image when used for execution (if it is not already prepared)
run_config.auto_prepare_environment = True

# specify CondaDependencies obj
run_config.environment.python.conda_dependencies = CondaDependencies.create(conda_packages=['scikit-learn'])

# Now submit a run on AmlCompute
from azureml.core.script_run_config import ScriptRunConfig

script_run_config = ScriptRunConfig(source_directory=project_folder, script='train.py', run_config=run_config)

run = experiment.submit(script_run_config)
run.wait_for_completion()