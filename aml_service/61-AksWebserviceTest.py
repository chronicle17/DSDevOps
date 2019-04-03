import numpy
import os, json, datetime, sys
from operator import attrgetter
from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.image import Image
from azureml.core.webservice import Webservice


# Get workspace
ws = Workspace.from_config()

# Get the AKS Details
try:
    with open("aml_config/aks_webservice.json") as f:
        config = json.load(f)
except:
    print('No new model, thus no deployment on ACI')
    #raise Exception('No new model to register as production model perform better')
    sys.exit(0)

service_name = config['aks_service_name']
# Get the hosted web service 
service=Webservice(workspace =ws, name = service_name)


# Input for old model
# input_j = [0.0,1.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.5,1.0,0.75,0.0,0.333]

# Input for Model with all features
input_j = [[1,2,3,4,5,6,7,8,9,10],[10,9,8,7,6,5,4,3,2,1]]
print(input_j)
test_sample = json.dumps({'data': input_j})
test_sample = bytes(test_sample,encoding = 'utf8')
try:   
    prediction = service.run(input_data = test_sample)
    print(prediction)
except Exception as e:
    result = str(e)
    print(result)
    raise Exception('AKS service is not working as expected')

# Delete aci after test
service.delete()
