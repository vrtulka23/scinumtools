"""
This script works in a similar way as pytests, but it is used to build code parts or generate tables.

Example of use:

python3 tools/generator/generator.py
python3 tools/generator/generator.py build_docs
python3 tools/generator/generator.py build_docs::build_temperature_units
"""
import sys, os
from io import StringIO
import importlib
import traceback

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

# set working path relative to this file
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# set environmental variables
os.environ["DIR_TESTS"] = "../../tests"
os.environ["DIR_SOURCE"] = "../../src"
os.environ["DIR_DOCS"] = "../../docs"
os.environ["DIR_TMP"] = "../../tmp"

def build():
    runonly = {}
    for path in sys.argv[1:]:
        if "::" in path:
            module, method = path.split("::")
        else:
            module, method = path, None
        if module not in runonly:
            runonly[module] = []
        if method:
            runonly[module].append(method)
            
    # run generator module
    for file_name in os.listdir():
        if file_name.startswith("build_"):
            module_name = file_name.replace(".py","")
            # run only selected modules
            if runonly and module_name not in runonly:
                continue
            module = importlib.import_module(module_name) 
            # run generator method
            print(f"{bcolors.HEADER}------ {module_name} ------{bcolors.ENDC}")
            for generator_name in dir(module):
                if generator_name.startswith("build_"):
                    # run only selected generators
                    if runonly and runonly[module_name] and generator_name not in runonly[module_name]:
                        continue
                    # run generator
                    try:
                        with Capturing() as output:
                            getattr(module,generator_name)()
                        if output:
                            output = "\n".join(output)
                            print(f"{bcolors.OKGREEN}{module_name}::{generator_name}{bcolors.ENDC}\n{output}")
                        else:
                            print(f"{bcolors.OKGREEN}{module_name}::{generator_name}{bcolors.ENDC}")
                    except Exception as error:
                        print(f"{bcolors.FAIL}{module_name}::{generator_name}{bcolors.ENDC}")
                        traceback.print_exc()
                        if output:
                            output = "\n".join(output)
                            print("\n"+output)
                            print(f"{bcolors.FAIL}{module_name}::{generator_name}{bcolors.ENDC}")
            print("")

if __name__ == "__main__":
    build()