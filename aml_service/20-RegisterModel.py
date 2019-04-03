import os, json,sys
from azureml.core import Workspace
from azureml.core import Run
from azureml.core import Experiment
from azureml.core.model import Model
from azureml.core.authentication import ServicePrincipalAuthentication

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

# Get the latest evaluation result 
try:
    with open("./aml_config/run_id.json") as f:
        config = json.load(f)
    if not config["run_id"]:
        raise Exception('No new model to register as production model perform better')
except:
    print('No new model to register as production model perform better')
    #raise Exception('No new model to register as production model perform better')
    sys.exit(0)

run_id = config["run_id"]
experiment_name = config["experiment_name"]
exp = Experiment(workspace = ws, name = experiment_name)

run = Run(experiment = exp, run_id = run_id)
names=run.get_file_names
names()
print('Run ID for last run: {}'.format(run_id))
model_local_dir="./model"
os.makedirs(model_local_dir,exist_ok=True)

# Download Model to Project root directory
model_name= 'sklearn_regression_model.pkl'
run.download_file(name = './outputs/'+model_name, 
                       output_file_path = model_local_dir+model_name)
print('Downloaded model {} to Project root directory'.format(model_name))

model = Model.register(model_path = model_local_dir+model_name, # this points to a local file
                       model_name = model_name, # this is the name the model is registered as
                       tags = {'area': "diabetes", 'type': "regression", 'run_id' : run_id},
                       description="Regression model for diabetes dataset",
                       workspace = ws)

print('Model registered: {} \nModel Description: {} \nModel Version: {}'.format(model.name, model.description, model.version))

# Remove the evaluate.json as we no longer need it
# os.remove("aml_config/evaluate.json")

# Writing the registered model details to /aml_config/model.json
model_json = {}
model_json['model_name'] = model.name
model_json['model_version'] = model.version
model_json['run_id'] = run_id
with open('./aml_config/model.json', 'w') as outfile:
  json.dump(model_json, outfile)
