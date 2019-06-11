# DevOps for Data Science Hands-On Lab
## Part 1 – Setup Environment
#### Setup AzureML Services Workspace
1. Navigate to http://portal.azure.com. Click Create a Resource and enter “machine learning” in the search box
![img1](./lab/images/img01.png)
2. Choose Machine Learning Service Workspace and click Create
![img2](./lab/images/img02.png)
3. Enter a workspace name, the resource group and region, and click Create
![img3](./lab/images/img03.png)

#### Setup Service Principal
1.	In the Azure Portal (http://portal.azure.com ), click the Search button on the top bar
![img4](./lab/images/img04.png)
2.	Search for “Azure Active Directory” and select the option under Services:
![img5](./lab/images/img05.png)
3.	Click “App Registrations” on the left, then click “New application registration”
![img6](./lab/images/img06.png)
4.	Enter the name of your application, and a URL.  For convenience and ease of tracking, we suggest you use you’re a unique prefix to your service principals.  The URL doesn’t have to be a real URL, you can enter http://invalid
![img7](./lab/images/img07.png)
5.	Once complete, click on the Certificates & Secrets button for your service principal then click Keys
![img8](./lab/images/img08.png)
6.  Click New Client Secret
![img8a](./lab/images/img08a.png)
7.	Here we will create a password for your service principal.  Enter “accessKey” for the description, and 1 year for the expiration.  Then click Add.  Once you click Add, the password will be displayed only once.  Copy the password before leaving the blade, otherwise you won’t be able to see it again.  Be sure to copy the Application ID as well, as we’ll need that later on.
![img9](./lab/images/img09.png)
8.	Retrieve the Tenant ID.  We’ll need this later.  On the left-hand blade, click “Overview” to show the properties of your Azure Active Directory.  Copy the Directory (Tenant) ID.  This is your Tenant ID.
![img10](./lab/images/img10.png)
9.	Now we need to give access for the Service Principal to use the AzureML Workspace.  Open the AzureML Workspace you created, click Access control (IAM) and Add a role assignment to add a user to a role.
![img11](./lab/images/img11.png)
10.	Choose Contributor for the role and enter the name of the service principal you created, then click save.
![img12](./lab/images/img12.png)

## Part 2 - Build Azure DevOps Pipeline
1.	Open a browser window and navigate to https://visualstudio.microsoft.com/
2. Under Azure DevOps (formerly VSTS) click “Get started for free”
![img13](./lab/images/img13.png)
3.	Once you sign in with a Microsoft user account, enter a project name and choose Private to create a new project
![img14](./lab/images/img14.png)
4.	Once the project is created, click Repos on the left navigation bar
![img15](./lab/images/img15.png)
5.	Click import to import a Git registry, enter https://github.com/chronicle17/DSDevOps, and click Import
![img16](./lab/images/img16.png)
6.	Click Pipelines and then New Pipeline to create a new build
![img17](./lab/images/img17.png)
7.	Select Azure Repos Git, then select the project and repository that you just created and click Continue
![img18](./lab/images/img18.png)
8.	When asked to select a template, choose Empty job
![img19](./lab/images/img19.png)
9.	Enter “Train Model” for the name and choose “Hosted Ubuntu 1604” for the agent pool
![img20](./lab/images/img20.png)
10.	Click on Agent job 1. Change the name to Run Pipeline and click the plus sign to add a task
![img21](./lab/images/img21.png)
11.	In the Add tasks blade, search for python in the search box and add Use Python Version
![img22](./lab/images/img22.png)
12.	Change the name to Use Python 3.6 and enter 3.6 in the Version spec
![img23](./lab/images/img23.png)
13.	Click the plus sign to add a task to the pipeline, search for command, and add Command line
![img24](./lab/images/img24.png)
14.	Change the Display name to “Install Python Packages”.  In the Script box, enter
“pip install -r ./environment_setup/requirements.txt”  
This will ensure that our build server has all of the packages that we need to build our model.
![img25](./lab/images/img25.png)
15.	Add a task to the pipeline. Search for python and choose Python Script
![img26](./lab/images/img26.png)
16.	Change the name to “Train Model on Local” and choose the script path “aml_service/10-TrainOnLocal.py”
17.	Add another Python script to the pipeline.  Change the name to Evaluate Model and the script path to “aml_service/15-EvaluateModel.py”
18.	Add 4 more Python scripts to the pipeline (hint, you can click Add multiple times)
![img27](./lab/images/img27.png)
19.	Fill out the remaining python scripts with following names and script path  

|name | script path|
|---- | ------------|
|Register Model    | aml_service/20-RegisterModel.py      |
|Create Scoring Image   | aml_service/30-CreateScoringImage.py  |
|Deploy to ACI   | aml_service/50-deployOnAci.py  |
|Test Deployment | aml_service/60-AciWebserviceTest.py |

20.	Your final pipeline should look like below:
![img28](./lab/images/img28.png)
21.	Now we have to set our environment variables. At the top, click Variables.
![img29](./lab/images/img29.png)
22.	In our scripts, we have environment variables for APPID, AZUREML_PASSWORD, RESOURCE_GROUP, SUBSCRIPTION, TENANT_ID, and WORKSPACE_NAME.  The APPID and AZUREML_PASSWORD are for the service principal that you created earlier on.
23.	Click Add and set the name to “APPID” and paste in the application id for the service principal we created.
![img30](./lab/images/img30.png)
24.	Add a variable “AZUREML_PASSWORD” and paste the password that you copied when you created the service principal
25.	Add a variable for “TENANT_ID” and paste in the Directory ID that you copied above when creating the service principal
26.	Add environment variable for “RESOURCE_GROUP”, “WORKSPACE_NAME”, and “SUBSCRIPTION”. These are the resource group that your AzureML Workspace is in, the name of your AzureML Workspace, and your subscription ID.
![img31](./lab/images/img31.png)
27.	Your environment variables should look like below
![img32](./lab/images/img32.png)
28.	At the top, click Save & queue, then Save & queue from the dropdown
![img33](./lab/images/img33.png)
29.	On the popup, click Save & queue
30.	To monitor the build, click on the build number in the top
![img34](./lab/images/img34.png)

Your pipeline run should look like the following:
![img35](./lab/images/img35.png)
### Congratulations, you just built a devops pipeline to build & deploy a machine learning model!
---

## Post Workshop Challenge
Most devops pipelines have a dev build and a release to production.  Treat the build pipeline that you just created as your dev build.  Create a release that uses your development pipeline, triggers a user approval for, then pushes the image and trained model to a production release. (hint, in Azure DevOps, explore the Releases tab)
https://docs.microsoft.com/en-us/azure/devops/pipelines/release/?view=azure-devops

