Hyperparameter tuning with Optuna
=================================

`Optuna <https://optuna.org/>`_ is a popular Python library for hyperparameter
optimization. In this guide you'll learn to optimize an `XGBoost <https://xgboost.readthedocs.io/en/latest/>`_ classification model with Optuna and scale your work using Dask and Coiled.

Before you start
----------------

You'll first need install the necessary packages, For the purposes of this example, we'll do this in a new virtual environment, but you could also install them in whatever environment you're already using for your project.

.. code:: bash

    $ conda create -n optuna-example -c conda-forge python=3.9 optuna xgboost coiled dask pip
    $ conda activate optuna-example
    (optuna-example) $ pip install dask-optuna

You also could use pip, or any other package manager you prefer; conda isn't required.

When you create a cluster, Coiled will automatically replicate your local `optuna-example` environment in your cluster (see :doc:`../package_sync`).

Optuna in a nutshell
--------------------

Optuna has three main concepts:

- Objective function: This is a function that depends on the hyperparameters
  in your model that you would like to optimize. For example, it's common to
  maximize a classification model's prediction accuracy (i.e. the objective
  function would be the accuracy score).

- Trial: a single evaluation of the objective function
  with a given set of hyperparameters.

- Study: a collection of optimization trials where each
  trial uses hyperparameters sampled from a set of allowed values.

The set of hyperparameters for the trial which gives the optimal value for the
objective function are chosen as the best set of hyperparameters.

Scaling Optuna with Dask
------------------------

In this guide, you'll use Optuna to optimize several hyperparameters for an
XGBoost classifier trained on the
`breast cancer dataset <https://scikit-learn.org/stable/datasets/toy_dataset.html#breast-cancer-wisconsin-diagnostic-dataset>`_.
You'll also use `Dask-Optuna <https://jrbourbeau.github.io/dask-optuna>`_ and
`Joblib <https://joblib.readthedocs.io/en/latest/>`_ to run Optuna trials in
parallel on a Coiled cluster.

Click :download:`here <optuna-example.py>` to download this example.

.. literalinclude:: optuna-example.py

And with that, you're able to run distributed hyperparameter optimizations using
Optuna, Dask, and Coiled! For more details on using Optuna, Dask, and Coiled,
check out `this Coiled blog post <https://coiled.io/blog/scalable-hyperparameter-optimization-optuna-dask/>`_.
