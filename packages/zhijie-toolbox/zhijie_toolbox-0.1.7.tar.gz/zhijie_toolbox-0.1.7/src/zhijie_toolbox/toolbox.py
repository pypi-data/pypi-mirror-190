import os
import shutil
from time import gmtime, strftime

def create_package_template(current_path, project_name, version="0.0.1", license_type="MIT"):
    # create src folder
    src_path = os.path.join(current_path, "src")
    os.makedirs(src_path, exist_ok=True)
    # create project folder
    project_path = os.path.join(src_path, project_name)
    os.makedirs(project_path, exist_ok=True)
    # create __init__.py example.py
    init_file_path = os.path.join(project_path, "__init__.py")
    example_file_path = os.path.join(project_path, "example.py")
    with open(init_file_path, mode='a'): pass
    with open(example_file_path, mode='a'): pass
    if license_type == "MIT":
        license = """MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
    else:
        license=""
    # create other necessary files and folder
    with open(os.path.join(current_path, "LICENSE"), mode='w') as f: 
        f.write(license)
    
    pyproject_template =  ["[build-system] \n", 
                           "requires = [\"setuptools>=61.0\"] \n", 
                           "build-backend = \"setuptools.build_meta\" \n",
                           "\n"
                           "[project] \n",
                           "name = \"{}\" \n".format(project_name),
                           "version = \"{}\" \n".format(version),
                           "authors = [ \n",
                           "{ name=\"Example Author\", email=\"author@example.com\" }, \n",
                           "]\n",
                           "description = \"A small example package\" \n",
                           "readme = \"README.md\" \n",
                           "requires-python = \">=3.7\" \n", 
                           "classifiers = [ \n",
                           "\"Programming Language :: Python :: 3\",\n",
                           "\"License :: OSI Approved :: MIT License\",\n",
                           "\"Operating System :: OS Independent\", \n",
                           "]\n",
                           "\n",
                           "[project.urls]\n",
                           "\"Homepage\" = \"https://github.com/pypa/sampleproject\"\n",
                           "\"Bug Tracker\" = \"https://github.com/pypa/sampleproject/issues\" \n"]
    with open(os.path.join(current_path, "pyproject.toml"), mode='w') as f: 
        f.writelines(pyproject_template)
        
    with open(os.path.join(current_path, "README.md"), mode='w'): pass
    os.makedirs(os.path.join(current_path, "tests"), exist_ok=True)
    
    
def version_control(current_path, runs_name, not_save_list=[".git", "runs"], log=""):
    """This is a simple version control function that copy current codes and save it into a specified folder

    Args:
        current_path (str): The top level code directory
        runs_name (str): Version control runs name
        not_save_list (list, str): Define the not copy files name, Defaults to ["runs"].
        log (str, optional): Add this version log, Defaults to "".
    """
    # create runs folder
    runs_path = os.path.join(current_path, "runs")
    os.makedirs(runs_path, exist_ok=True)
    # create current runs folder with the name of runs_name
    runs_name_path = os.path.join(runs_path, runs_name)
    os.makedirs(runs_name_path)
    # get all the list file in current path
    dirs = os.listdir(current_path)
    print("Runs name path", runs_name_path)
    
    if "runs" not in not_save_list:
        not_save_list.append("runs")

    log = strftime("%Y-%m-%d %H:%M:%S", gmtime()) +"\n"+ log
    with open(os.path.join(runs_name_path, "log.txt"), mode='w') as f: 
        f.write(log)
        
    for file in dirs:
        if file not in not_save_list:       
            source = os.path.join(current_path, file)
            destination =  os.path.join(runs_name_path, file)
            
            if os.path.isfile(source):
                # copy these file to runs_path
                shutil.copy(os.path.join(current_path, file), os.path.join(runs_name_path, file))
            else:
                shutil.copytree(source, destination)
                

def create_project_template(current_path, add_folder=None):
    """Define a project template: in the top level directory: 
    configs: store package template
    datasets: store neceesary datasets
    experiments: store experiment result and also checkpoint
    scripts: runnning files
    test: testing files folder
    packages: store the main model and algorithm

    Args:
        current_path (str): path to create project template
        add_folder (str): if needs to add other folders
    """
    # create necessary 
    folders = ["configs", "datasets", "experiments", "scripts", "tests", "packages"]
    if add_folder is not None:
        folders += add_folder
    
    
    ReadMe = "README.md"
    for folder in folders:
        folder_path = os.path.abspath(os.path.join(current_path, folder))
        os.makedirs(folder_path, exist_ok=True)
        ReadMe_path = os.path.abspath(os.path.join(folder_path, ReadMe))
        with open(ReadMe_path, mode='a'): pass
    
    