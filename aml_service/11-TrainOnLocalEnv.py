## Create a new Conda environment on local and train the model
## System-managed environment

from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import RunConfiguration
from azureml.core import Workspace
from azureml.core import Experiment
from azureml.core import ScriptRunConfig

# Get workspace
ws = Workspace.from_config()

# Attach Experiment
experiment_name = 'devops-ai'
exp = Experiment(workspace  = ws, name = experiment_name)
print(exp.name, exp.workspace.name, sep = '\n')

# Editing a run configuration property on-fly.
run_config_system_managed = RunConfiguration()
# Use a new conda environment that is to be created from the conda_dependencies.yml file
run_config_system_managed.environment.python.user_managed_dependencies = False
# Automatically create the conda environment before the run
run_config_system_managed.prepare_environment = True

# # add scikit-learn to the conda_dependencies.yml file
# Specify conda dependencies with scikit-learn
# run_config_system_managed.environment.python.conda_dependencies = CondaDependencies.create(conda_packages=['scikit-learn'])

print("Submitting an experiment to new conda virtual env")
src = ScriptRunConfig(source_directory = './code', script = 'training/train.py', run_config = run_config_user_managed)
run = exp.submit(src)

# Shows output of the run on stdout.
run.wait_for_completion(show_output = True)

# Writing the run id to /aml_config/run_id.json
run_id = {}
run_id['run_id'] = run.id
run_id['experiment_name'] = run.experiment.name
with open('aml_config/run_id.json', 'w') as outfile:
  json.dump(run_id,outfile)
