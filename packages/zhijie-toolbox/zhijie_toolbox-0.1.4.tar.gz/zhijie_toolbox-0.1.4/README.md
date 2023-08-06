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