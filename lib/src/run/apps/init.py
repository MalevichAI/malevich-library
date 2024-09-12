from malevich.square import Context, init
import sys
import subprocess
from importlib import import_module

# Function to install a package using pip
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
@init()
def import_modules(context: Context):
    deps = context.app_cfg.get('dependencies', None)
    if deps and isinstance(deps, list[str]):
        for package in deps:
            install_package(package)
        deps = {dep: import_module(dep) for dep in deps}
        context.app_cfg['dependencies'] = deps