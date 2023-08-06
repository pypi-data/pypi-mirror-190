# Project description

## Install
`pip install zhijie_toolbox`

## Method
- create_package_template(current_path, project_name, version="0.0.1", license_type="MIT")

This will help you to create a package template that speed up publishing package.

Usage:
```
from zhijie_toolbox import toolbox
toolbox.create_package_template(current_path, project_name)
```

- version_control(current_path, runs_name, not_save_list=[".git", "runs"], log="")

This will help you to copy current codes to a runs folder where we can record our codes locally
We can define not save list by ourself by specify files name

Usage:
```
from zhijie_toolbox import toolbox
toolbox.version_control(current_path, runs_name)
```

- create_project_template(current_path, add_folder=None)

This function will help you create a project template. 
Basic folders are ["configs", "datasets", "experiments", "scripts", "tests", "packages"]

Usage:
```
from zhijie_toolbox import toolbox
toolbox.create_project_template(current_path)
```
