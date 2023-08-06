# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aima', 'aima.hobs']

package_data = \
{'': ['*'], 'aima': ['images/*']}

install_requires = \
['ipythonblocks>=1.9,<2.0', 'jupyter>=1.0,<2.0', 'pandas>=1.5,<2.0']

entry_points = \
{'console_scripts': ['aima = aima.main:main']}

setup_kwargs = {
    'name': 'aima',
    'version': '2023.2.6',
    'description': 'Artificial Intelligence a Modern Approach 4th Ed by Peter Norvig and Stuart Russel',
    'long_description': '# Introduction\n\nCode for Artificial Intelligence: A Modern Approach (AIMA) 4th edition by Peter Norvig and Stuart Russel.\n\nShameless reuse of Norvig\'s official repository at https://github.com/aimacode/aima-python/ \n\nThe code should work in Python 3.7+.\n\n# How to Browse the Code\n\nYou can get some use out of the code here just by browsing, starting at the root of the source tree or by clicking on the links in the index on the project home page. The source code is in the .py files; the .txt files give examples of how to use the code.\n\n# How to Install the Code\n\nIf you like what you see, install the code using either one of these methods:\n\nFrom a command shell on your computer, execute the svn checkout command given on the source tab of the project. This assumes you have previously installed the version control system Subversion (svn).\nDownload and unzip the zip file listed as a "Featured download"on the right hand side of the project home page. This is currently (Oct 2011) long out of date; we mean to make a new .zip when the svn checkout settles down.\n\nYou\'ll also need to install the data files from the aima-data project. These are text files that are used by the tests in the aima-python project, and may be useful for yout own work.\n\nYou can put the code anywhere you want on your computer, but it should be in one directory (you might call it aima but you are free to use whatever name you want) with aima-python as a subdirectory that contains all the files from this project, and data as a parallel subdirectory that contains all the files from the aima-data project.\n\n# How to Test the Code\n\nFirst, you need to install Python (version 2.5 through 2.7; parts of the code may work in other versions, but don\'t expect it to). Python comes preinstalled on most versions of Linux and Mac OS. Versions are also available for Windows, Solaris, and other operating systems. If your system does not have Python installed, you can download and install it for free.\n\nIn the aima-python directory, execute the command\n\n    python doctests.py -v *.py\n\nThe "-v" is optional; it means "verbose". Various output is printed, but if all goes well there should be no instances of the word "Failure", nor of a long line of "". If you do use the "-v" option, the last line printed should be "Test passed."\n\n# How to Run the Code\n\nYou\'re on your own -- experiment! Create a new python file, import the modules you need, and call the functions you want.\n\n# Acknowledgements\n\nMany thanks for the bug reports, corrected code, and other support from Phil Ruggera, Peng Shao, Amit Patil, Ted Nienstedt, Jim Martin, Ben Catanzariti, and others.\n',
    'author': 'Peter Norvig (norvig)',
    'author_email': 'peter.norvig@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/tangibleai/community/aima',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
