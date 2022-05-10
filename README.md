# Hanabi Agent Explanation

## Introduction

This repo contains the implementation of the methdology proposed
in the thesis "The card game Hanabi as a domain for explainable AI".

## Environment Setup

We use [jupyter notebooks](https://jupyter.org/install) as our interactive development environment.
These environments are also provided by platforms such as
[Google Colaboratory](https://research.google.com/colaboratory), [Kaggle Notebooks](https://www.kaggle.com/code), and [Gradient Notebooks](https://gradient.run/notebooks).
The most recent snapshots of notebooks are provided as HTML webpages.

## Code Structure

For an overview of explanation methodology, please refer to
Figures 2.1 and 3.2 of the thesis.

`off-belief-small` is a modified version of the `off-belief-learning`
implementation from Facebook Research, with modifications made to
enable [Hanabi-Small](https://github.com/deepmind/hanabi-learning-environment/blob/master/hanabi_learning_environment/rl_env.py#L548) compatibility.
It is used in the `agent-training-small` and `observation-extraction`
notebooks to train and observe agents on 2-player Hanabi-Small.

`observation-datasets` consists of the raw state-action datasets
generated from `observation-extraction`.

`rule-list-learning` contains a collection of transformed datasets
produced in `oracle-transformation`, using feature construction.
It also includes [BioHEL](https://ico2s.org/software/biohel.html), the decision list learner used in
`rule-learning`, and its decision list learning logs.

Lastly, `sample-explanations` includes examples of decision lists
that attempt to explain the OBL agent's behaviour in standard Hanabi,
which are derived from the logs created in the `rule-learning` notebook.
