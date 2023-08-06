import os, sys
current_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
package_root = os.path.join(project_root, "src")
sys.path.append(package_root)

from zhijie_toolbox import toolbox

# toolbox.create_package_template(current_path, "test_project")
# toolbox.version_control(current_path, runs_name="A2")

toolbox.create_project_template(current_path, ["yes", "no"])