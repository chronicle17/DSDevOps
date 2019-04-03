from azureml.core import Workspace
import os, json
import azureml.core
print("SDK Version:", azureml.core.VERSION)
#print('current dir is ' +os.curdir)
with open("aml_config/config.json") as f:
    config = json.load(f)

workspace_name = config['workspace_name']
resource_group = config['resource_group']
subscription_id = config['subscription_id']
location = 'southcentralus'
try:
    ws = Workspace.get(name = workspace_name,
                             subscription_id = subscription_id,
                             resource_group = resource_group)

except:
    # this call might take a minute or two.
    ws = Workspace.create(name = workspace_name,
                             subscription_id = subscription_id,
                             resource_group = resource_group,
                             #create_resource_group=True,
                             location=location)

# print Workspace details 
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep = '\n')