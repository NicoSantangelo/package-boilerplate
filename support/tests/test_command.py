#  Remember to install AAAPT package to run the tests

import unittest
from {PackageName} import {package_name}

# To reload your tests every time you save your command file, add the following to it:
# for test_file in glob.glob("tests/test_*.py"):
#     key = "{PackageName}." + test_file[:-3].replace("/", ".")
#     if key in sys.modules:
#         reload(sys.modules[key])

class Test_{PackageName}Command(unittest.TestCase):
    pass