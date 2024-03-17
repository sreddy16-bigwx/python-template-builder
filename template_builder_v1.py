#############################################################################################
# Python script 
# Bigwx
# version: 1.0
#############################################################################################

#********************************************************************************************
# Import packages
#********************************************************************************************
import os
import subprocess
import json

#********************************************************************************************
# Security Updates 
#********************************************************************************************
# Pat Token for GitHub and Retrieve the token from the environment variable
token = os.environ.get("GITHUB_PAT_TOKEN")

if token is None:
    print("Error: GitHub PAT token not found in environment variable GITHUB_PAT_TOKEN")
    exit(1)

print("==========================================================================================")
print("Python template builder for Backstage")
print("Bigwx")
print("==========================================================================================")

#********************************************************************************************
# GitHub References
#********************************************************************************************
# Source Repo
source_repo_url = "https://github.com/sreddy16-bigwx/builder-templates.git"
# Source repo to place in a folder
source_repo_dir = "temp-source"
# update with the pat token to clone and further access
source_repo_url_with_token = source_repo_url.replace("https://", f"https://{token}@")
subprocess.run(["git", "clone", source_repo_url_with_token, source_repo_dir])
# Destination Repo
destination_repo_url = "https://github.com/sreddy16-bigwx/builder-templates-bs.git"
# Destination repo to place in a folder
destination_repo_dir = "temp-destination"
# update with the pat token to clone and further access
destination_repo_url_with_token = destination_repo_url.replace("https://", f"https://{token}@")
subprocess.run(["git", "clone", destination_repo_url_with_token, destination_repo_dir])

print("-----------------------------------------------------------------------------------------")
print("success : Git repos has been Succusfully cloned")             
print("-----------------------------------------------------------------------------------------")
#********************************************************************************************
# Extract the Parameters from the Json files in the Pattern folder
#********************************************************************************************

# function to parse through the json files and search for a pattern
def parse_json_and_extract_parameters(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)
        properties = data.get("properties", {})
        #property_type = data.get("type","")
        #parameter_types = [param["type"] for param in parameters]
        #type_value = data["properties"]["type"]
        type_value = properties.get("type", "")
        version_value = properties.get("version", "") 
        parameters = properties.get("parameters", [])
        parameter_names = [param.get("name", "") for param in parameters]
        print("Parameter names:", parameter_names)
        return parameter_names, type_value, version_value

# Define paths
patterns_folder = os.path.join(source_repo_dir, "patterns")
#print(patterns_folder)
template_build_path = os.path.join(destination_repo_dir, "template-build.yaml")


###
if not os.path.exists(template_build_path):
    with open(template_build_path, "w") as template_build_file:
        pass  # This will create an empty file

##
#print(template_build_path)
# Extract parameter names from JSON files in patterns folder
all_parameter_names = []
for root, dirs, files in os.walk(patterns_folder):
    for file in files:
        if file.endswith(".json"):
            json_file_path = os.path.join(root, file)
            #print(json_file_path)
            parameter_names,type_value,version_value = parse_json_and_extract_parameters(json_file_path)
            print("-----------------------------------------------------------------------------------------")
            print("The Parameters ")  
            print("-----------------------------------------------------------------------------------------")
            print(json_file_path, ": Parameters are " ,parameter_names)
            print("-----------------------------------------------------------------------------------------")
            all_parameter_names.extend(parameter_names)    
print("&&&&&&&&&&")
print("Type value:", type_value)   
print("-----------------------")
print("Type value:", parameter_names)  
print("-----------------------")
print("Type value:", version_value)  
print("&&&&&&&&&&")    
# Generate content for temp late-build.yaml based on parameter names
template_content = f"  parameters:\n"
for parameter_name in all_parameter_names:
    template_content += f"  #  Parameters varaiable values\n"
    template_content += f"    - title: Fill in some steps\n"
    template_content += f"      required:\n"
    template_content += f"        - {parameter_name}\n"
    template_content += f"      properties:\n"
    template_content += f"        {parameter_name}:\n"
    template_content += f"          title: {parameter_name}\n"
    template_content += f"          type: string\n"
    template_content += f"          description: Unique name for your {parameter_name}\n"
    template_content += f"          ui:autofocus: true\n"
    template_content += f"          ui:options:\n"
    template_content += f"            rows: 5\n"
    template_content += f"\n"

print("-----------------------------------------------------------------------------------------")
print("success : Extracted the required Parameters and updated the template content")             
print("-----------------------------------------------------------------------------------------")

# Write template content to template-build
with open(template_build_path, "r") as template_build_file:
    existing_content = template_build_file.read()
#### print(existing_content)
# Find the index where "parameters" section ends
#0001 - parameters_index = existing_content.find("#Adding the content")
#0001 - parameters_end_index = existing_content.find("\n", parameters_index)

# Append the new parameters content after the existing "parameters" section
#0001 - updated_content = existing_content[:parameters_end_index + 1] + template_content + existing_content[parameters_end_index + 1:]

# Write template content to template-build
#0001 - with open(template_build_path, "w") as template_build_file:
    #template_build_file.write(template_content)
    #0001 - template_build_file.write(updated_content)
#********************************************************************************************
# Get the base Template from the base folder
#********************************************************************************************

file_paths = []
# Define the file paths in repo1
folders = ["base",]# "patterns"]
for folder in folders:
    for filename in os.listdir(os.path.join(source_repo_dir, folder)):
        file_paths.append(os.path.join(source_repo_dir, folder, filename))
#print("step--07")
# Combine content from files into template-build.yaml
combined_content = ""
for file_path in file_paths:
    with open(file_path, "r") as file:
        combined_content += file.read() + "\n"

parameters_index_01 = combined_content.find("#Adding the content")
parameters_end_index_01 = combined_content.find("\n", parameters_index_01)

# Append the new parameters content after the existing "parameters" section
backstage_content = combined_content[:parameters_end_index_01 + 1] + template_content + combined_content[parameters_end_index_01 + 1:]
#print("===========FINAL : BACKSTAGE TEMPLATE START ========================")
#print(backstage_content)
#print("===========FINAL : BACKSTAGE TEMPLATE END========================")

print("-----------------------------------------------------------------------------------------")
print("success : Extracted the required Template and updated it with parameters ")             
print("-----------------------------------------------------------------------------------------")

# Write combined content to template-build.yaml
template_build_path = os.path.join(destination_repo_dir, "template-build.yaml")
with open(template_build_path, "w") as template_build_file:
   # template_build_file.write(combined_content)
   # template_build_file.write(updated_content)
    template_build_file.write(backstage_content)

#3 with open(os.path.join(destination_repo_dir, "template-build.yaml"), "a") as template_build_file:
#3    template_build_file.write(template_content)
#********************************************************************************************
# git actions to push the code to the gitHub repos
#********************************************************************************************
os.chdir(destination_repo_dir)
#print("Current working directory:", os.getcwd())
result = subprocess.run(["git", "add", os.path.join("..", destination_repo_dir, "template-build.yaml")], capture_output=True, text=True)
if result.returncode != 0:
    #print("Error:", result.stderr)
    print("There is no error at moment")
try:
    #subprocess.run(["git", "add", os.path.join("..", destination_repo_dir, "template-build.ppp")])
    subprocess.run(["git", "add", "template-build.yaml"])
    #print("git-add")
    subprocess.run(["git", "commit", "-m", "Add template-build file"])
    #print("git-commit")
    subprocess.run(["git", "push", "origin", "main"])
    subprocess.run(["git", "status"])
    #print("template-build.ppp has been created and pushed to repo.")
except subprocess.CalledProcessError as e:
    print("Error executing Git commands:", e)
print("-----------------------------------------------------------------------------------------")
print("upstream to Git repos")             
print("-----------------------------------------------------------------------------------------")
print("Succussfully copied the content and created the Template")
print("===============================================================================")