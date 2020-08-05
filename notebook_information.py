"""
Author: Alexander Hoch
Date: 25.04.2020 (adapted at 30.06.2020)
Github: https://github.com/AlexH-UB/JNotebookInformation
Version: 1.0

Use: Print all necessary details that need to be displayed at the top of a jupyter notebook including:

1. Python version and environment name

2. Version number of all packages in use

3. Last time Executed

"""

import sys
import types
from datetime import datetime


def import_jupyter_modules(jupyter_namespace: dict) -> list:
    """This function retrieves the import statements of your notebook by checking in its namespace. The return is a list
    of import statements like "import pandas as pd"
    :param jupyter_namespace: copy of the jupyter notebook global namespace
    :return: list of import statements as strings
    """
    assert ('# Import block' in jupyter_namespace) and ('# Input' in jupyter_namespace), 'For the use of this' \
                                                                                         'function please use "# ' \
                                                                                         'Import block" and "# Import' \
                                                                                         ' end"' \
                                                                                         ' in your cell. '

    # Find position of the statements in the cell
    x = jupyter_namespace.index('# Import block')
    y = jupyter_namespace.index('# Import end')

    # Split test and retrieve import statements
    module_list = jupyter_namespace[x + 14:y].split('\n')
    while '' in module_list:
        module_list.remove('')
    return module_list


def access_notebook_information(global_namespace: dict, env: dict):
    """A function to print the python version you are using, the environment name, the packages and their versions
    and the last run time.

    For this code to run you need to create a separate section in your code to import all modules you need that
    starts with "# Import block" and ends with "# Import end".

    :param global_namespace: Enter your global namespace (Usually enter: dict(globals())['_ih'][1])
    :param env: Enter your env you can get with the magic command %env. Set
    this to a variable and enter the variable here.
    :return: Prints the above written information
    """
    module_list = import_jupyter_modules(global_namespace)

    name_version_dict = {}
    for module in module_list:

        split_name = module.split(' ')

        # Name of the module is always on second position
        m_name = split_name[1].split('.')[0]
        s_name = m_name

        try:
            exec(f'from {m_name} import __version__ as {m_name}_version')
            version = eval(f'{m_name}_version')
        except:
            continue

        if 'as' in module:
            s_name = f'{m_name} ({split_name[-1]})'
        if m_name not in name_version_dict.keys():
            name_version_dict[s_name] = version

    # Print all information gathered

    # Python version and environment name
    s = (f"Python Version:\t{sys.version.split('|')[0]}, "
         f"environment: {env['CONDA_PROMPT_MODIFIER'].split(')')[0][1:]}\n\nPackages:\n")

    # Package versions of imported modules
    for name, version in name_version_dict.items():
        s += f'{name}:\t{version}\n'.expandtabs(30)

    # Last time the Code ran
    s += f'\nLast execution time: {str(datetime.now())[:-10]}\n'

    print(s)
