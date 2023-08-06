from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.3'
DESCRIPTION = 'Libreria de Redes Bayesianas'

# Setting up
setup(
    name="RedesBayesianas_18364_18761",
    version=VERSION,
    author="Jorge Perez y Diego Ruiz",
    author_email="<per18364@uvg.edu.gt>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['numpy', 'pyAgrum'],
    keywords=['python', 'bayes', 'bayesian network'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
