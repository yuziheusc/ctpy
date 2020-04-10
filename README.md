# CTPY: A Python Interface for R Causal Tree

## Introduction
This package is a interface for the R implementation of causal tree. 
This package relies on rpy2, which runs embedded R session in a pyhton process.

## Features
Support constructing, pruning and ploting of causal trees. Any parameter available for constructing causal trees is supported.

## Installation

### 1. Install R and causal tree library
For R installation, please check with manual of your OS.
Installation of causal tree library can be found at the following repository:
https://github.com/susanathey/causalTree

### 2. Install rpy2
```shell
pip install rpy2
```

### 3. Install ctpy
Download with
```shell
git clone https://github.com/yuziheusc/ctpy
```

## Example
The following code shows how to construct a causal tree, performing pruning using cross validation and plot it. The R code of this example is available at https://github.com/susanathey/causalTree
```python
from ct_r import causal_tree_r
from rpy2.robjects.packages import importr
import rpy2.robjects as robjects

## get data provided by causal tree r package
causalTree = importr('causalTree')
df = robjects.r("simulation.1")

## define features, treament and outcome
features = ["x1", "x2", "x3", "x4"]
outcome = "y"
treat = "treatment"
params = {
    "split.Rule":"CT",
    "split.Honest":True,
    "cv.option":"matching",
    "cv.Honest":False,
    "split.Bucket":False,
    "xval":10,
}

ct = causal_tree_r()
ct.tree_setup(df, features, outcome, treat, params)
cp_res = ct.show_cp_table()
ct.plot_tree(file="tree_org.png")
ct.prune("auto")
ct.plot_tree(file="tree_pru.png")
```

## Additional Note
1. I did not find a way to get prediction y(x|t=0) and y(x|t=1) from the R code

2. Causal forest feature will be added!

