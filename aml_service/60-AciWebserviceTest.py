import numpy
import os, json, datetime, sys
from operator import attrgetter
from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.image import Image
from azureml.core.webservice import Webservice
from azureml.core.webservice import AciWebservice
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

# Get the ACI Details
try:
    with open("./aml_config/aci_webservice.json") as f:
        config = json.load(f)
except:
    print('No new model, thus no deployment on ACI')
    #raise Exception('No new model to register as production model perform better')
    sys.exit(0)

service_name = config['aci_name']
# Get the hosted web service 
service=Webservice(name = service_name, workspace =ws)

# Input for old model
# input_j = [0.0,1.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.5,1.0,0.75,0.0,0.333]

# Input for Model with all features
input_j = [[0.0380759064334241,0.0506801187398187,0.0616962065186885,0.0218723549949558,-0.0442234984244464,-0.0348207628376986,-0.0434008456520269,-0.00259226199818282,0.0199084208763183,-0.0176461251598052],
           [-0.001882016527791,-0.044641636506989,-0.0514740612388061,-0.0263278347173518,-0.00844872411121698,-0.019163339748222,0.0744115640787594,-0.0394933828740919,-0.0683297436244215,-0.09220404962683]]
print(input_j)
test_sample = json.dumps({'data': input_j})
test_sample = bytes(test_sample,encoding = 'utf8')
try:   
    prediction = service.run(input_data = test_sample)
    print(prediction)
except Exception as e:
    result = str(e)
    print(result)
    raise Exception('ACI service is not working as expected')
