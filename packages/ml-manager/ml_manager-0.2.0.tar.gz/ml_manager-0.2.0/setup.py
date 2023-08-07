from setuptools import setup, find_packages
import codecs
import os

# here = os.path.abspath(os.path.dirname(__file__))

# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()

VERSION = '0.2.0'
DESCRIPTION = 'A manager which manages all your ML experiments'
LONG_DESCRIPTION = 'ml_manager is a managerial software which manages all ML experiments, it tracks losses and metrics, saves the history, makes training plots, makes up a different folder for every new experiment and also sends training alerts and updates on your telegram.'

# Setting up
setup(
    name="ml_manager",
    version=VERSION,
    author="Manoj Akondi",
    author_email="manojakondi25@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['torch', 'numpy', 'matplotlib', 'pandas'],
    keywords=['python', 'pytorch', 'Machine Learning', 'Deep Learning'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)