import os, json, sys
from azureml.core import Workspace
from azureml.core.image import ContainerImage, Image
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

# Get the latest model details

try:
    with open("./aml_config/model.json") as f:
        config = json.load(f)
except:
    print('No new model to register thus no need to create new scoring image')
    #raise Exception('No new model to register as production model perform better')
    sys.exit(0)

model_name = config['model_name']
model_version = config['model_version']


model_list = Model.list(workspace=ws)
model, = (m for m in model_list if m.version==model_version and m.name==model_name)
print('Model picked: {} \nModel Description: {} \nModel Version: {}'.format(model.name, model.description, model.version))

os.chdir('./code/scoring')
image_name = "diabetes-model-score"

image_config = ContainerImage.image_configuration(execution_script = "score.py",
                                                  runtime = "python",
                                                  conda_file = "conda_dependencies.yml",
                                                  description = "Image with ridge regression model",
                                                  tags = {'area': "diabetes", 'type': "regression"}
                                                 )

image = Image.create(name = image_name,
                     models = [model],
                     image_config = image_config,
                     workspace = ws)

image.wait_for_creation(show_output = True)
os.chdir('../..')

if image.creation_state != 'Succeeded':
  raise Exception('Image creation status: {image.creation_state}')

print('{}(v.{} [{}]) stored at {} with build log {}'.format(image.name, image.version, image.creation_state, image.image_location, image.image_build_log_uri))

# Writing the image details to /aml_config/image.json
image_json = {}
image_json['image_name'] = image.name
image_json['image_version'] = image.version
image_json['image_location'] = image.image_location
with open('./aml_config/image.json', 'w') as outfile:
  json.dump(image_json,outfile)


# How to fix the schema for a model, like if we have multiple models expecting different schema, 
