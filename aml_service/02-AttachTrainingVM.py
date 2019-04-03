
from azureml.core import Workspace
from azureml.core import Run
from azureml.core import Experiment
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import RunConfiguration
import os, json
from azureml.core.compute import RemoteCompute
from azureml.core.compute import DsvmCompute
from azureml.core.compute_target import ComputeTargetException


# Get workspace
ws = Workspace.from_config()

# Read the New VM Config
with open("aml_config/security_config.json") as f:
    config = json.load(f)

remote_vm_name = config['remote_vm_name']
remote_vm_username = config['remote_vm_username']
remote_vm_password = config['remote_vm_password']
remote_vm_ip = config['remote_vm_ip']

try:
    dsvm_compute = RemoteCompute.attach(ws, name=remote_vm_name, 
                                        username=remote_vm_username, 
                                        address=remote_vm_ip, 
                                        ssh_port=22, 
                                        password=remote_vm_password)
    dsvm_compute.wait_for_completion(show_output =True)

except Exception as e:
    print("Caught = {}".format(e.message))
    print("Compute config already attached.")


# Create VM if not available
# compute_target_name = 'mydsvm'

# try:
#     dsvm_compute = DsvmCompute(workspace=ws, name=compute_target_name)
#     print('found existing:', dsvm_compute.name)
# except ComputeTargetException:
#     print('creating new.')
#     dsvm_config = DsvmCompute.provisioning_configuration(vm_size="Standard_D2_v2")
#     dsvm_compute = DsvmCompute.create(ws, name=compute_target_name, provisioning_configuration=dsvm_config)
#     dsvm_compute.wait_for_completion(show_output=True)