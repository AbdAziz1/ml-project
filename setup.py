from setuptools import setup, find_packages
from typing import List

def get_requirements(file_path: str) -> List[str]:
    '''
    This function returns a list of requirements
    The requirements.txt file should be in the same directory as this setup.py file
    The requirements.txt file should contain the list of packages required to run the project
    in the below code, we are reading the requirements.txt file and removing the new line character from each line and also removing the '-e .' line if it exists and returning the list of requirements
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace('\n', '') for req in requirements]
        if '-e .' in requirements:
            requirements.remove('-e .')
        
    return requirements


setup(

name = 'mlproject',
version = '0.0.1',
author='Aziz',
author_email='azzizz10301@gmail.com',
packages=find_packages(),
install_requires = get_requirements('requirements.txt')


)