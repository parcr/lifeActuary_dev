import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plotcdf",  # Replace with your own username
    version="0.0.1",
    author="PedroCR",
    author_email="pedro.cortereal@magentakoncept.com",
    description='This python package allows us to plot beautiful cumulative distributions functions for '
                'discrete random variables.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/parcr/plotcdf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['matplotlib>=3.1',
                     'numpy>=1.16'],
    python_requires='>=3.6',
)
