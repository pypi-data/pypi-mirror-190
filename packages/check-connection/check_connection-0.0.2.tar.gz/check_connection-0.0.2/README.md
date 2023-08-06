# Template Project to create working pip package

This package contains an check_connection function where you can enter your server adress and the number of tries, so that it connects to the server as many times as given and calculates the artihmetic mean on how long it takes to do so.\
Additionally a list_mean function is implemented, where you can calculate the arithmetic mean of a list.


Also, this project is an example package to show how to create an own pip package.
In the following the steps to do so are explained



## 1. Sourcetree
The structure of the project has to contain the following files and folders:
    - LICENSE.txt
    - README.txt
    - CHANGELOG.txt
    - pyproject.toml
    - requirements.txt
    - src/{name_of_your_package}

Files such as .flake or Jenkinsfile are optional and can be used to check your code autmatically when updated on git.

## 2. Building

After setting up your sourcetree and implementing the code in `__init__.py` the build can be started by `py -m build`.\
This will created all needed files and structures. Afterwards this can be published to PyPi by `twine upload dist/*`.\
Consider that you have to have an existing PyPi Account and that your package name is not already used.

Now your package is finished and can be implement by other users by using `pip install {your_package_name}`

For further information see:\
https://confluencewikiprod.intra.infineon.com/display/SCCVMP/Basic+structure+of+a+python+Project \
https://packaging.python.org/en/latest/tutorials/packaging-projects/
