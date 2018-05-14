# Installation instructions for BIDSIFY

### Install Python using Anaconda

You first need a distribution of python, we highly recommend using the Anaconda 3.6 distribution which you can get from [here](https://www.anaconda.com/downloads).

### Get the Bidsify repository from Github

Clone the [Bidsify](https://github.com/nejaz1/bidsify) repository onto your system using the following commands. For example, in  MacOSX open up a terminal window and go to the directory you want to install PyPotamus in and type the following commands:

```
mkdir bidsify
git clone git@github.com:nejaz1/bidsify.git bidsify
```

### Install package dependencies for Bidsify

Use the condo package manager to setup a new environment and install the package dependencies specified in the `environment.yml` file using the following commands in terminal:

```
cd bidsify
conda env create -f environment.yml
```



