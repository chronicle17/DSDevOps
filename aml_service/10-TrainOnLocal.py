import azureml.core

from azureml.core.runconfig import RunConfiguration
from azureml.core import Workspace
from azureml.core import Experiment
from azureml.core import ScriptRunConfig
from azureml.core.authentication import ServicePrincipalAuthentication
import os, json

# Get workspace
# ws = Workspace.from_config()
svc_pr_password = os.environ.get("AZUREML_PASSWORD")
tenant = os.environ.get("TENANT_ID")
serviceprin = os.environ.get("APPID")
sub = os.environ.get("SUBSCRIPTION")
rg = os.environ.get("RESOURCE_GROUP")
wrkspc = os.environ.get("WORKSPACE_NAME")

svc_pr = ServicePrincipalAuthentication(
    tenant_id=tenant,
    service_principal_id=serviceprin,
    service_principal_password=svc_pr_password)


ws = Workspace(
    subscription_id=sub,
    resource_group=rg,
    workspace_name=wrkspc,
    auth=svc_pr
    )

print("Found workspace {} at location {}".format(ws.name, ws.location))

# Attach Experiment
experiment_name = 'devops-ai-demo'
exp = Experiment(workspace=ws, name=experiment_name)
print(exp.name, exp.workspace.name, sep='\n')

# Editing a run configuration property on-fly.
run_config_user_managed = RunConfiguration()
run_config_user_managed.environment.python.user_managed_dependencies = True

print("Submitting an experiment.")
src = ScriptRunConfig(source_directory='./code', script='training/train.py', run_config=run_config_user_managed)
run = exp.submit(src)

# Shows output of the run on stdout.
run.wait_for_completion(show_output=True)

# if run.get_status() != 'Completed':
#   raise Exception('Training on local failed with following run status: {}'.format(run.get_status()))

# Writing the run id to /aml_config/run_id.json

run_id={}
run_id['run_id'] = run.id
run_id['experiment_name'] = run.experiment.name
with open('./aml_config/run_id.json', 'w') as outfile:
    json.dump(run_id, outfile)
