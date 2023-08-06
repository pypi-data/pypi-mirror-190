====================
Polytechnique INF581
====================

Copyright (c) 2019-2021 Jérémie Decock

.. image:: logo.jpg
    :width: 100
    :alt: Alternative text


Github repository: https://github.com/jeremiedecock/polytechnique-inf581-2021


Moodle
======

    https://moodle.polytechnique.fr/course/view.php?id=9352


Welcome to INF581!
==================

Driven by recent breakthroughs, rapidly growing collections of data, and a plethora of exciting applications, artificial intelligence is experiencing massive interest and investment from both the academic and industrial scene.

This course selects a number of advanced topics to explore in machine learning and autonomous agents, in particular:

- Probabilistic graphical models (Bayesian networks, ...)
- Multi-output and structured-output prediction problems
- Deep-learning architectures
- Methods of search and optimization (Beam search, epsilon-approximate search, stochastic optimization, Monte Carlo methods, ...)
- Sequential prediction and decision making (HMMs, Sequential Monte Carlo, Bayesian Filtering, MDPs, ...)
- Reinforcement learning (Q-Learning, Deep Q-Learning, ...)

Although these topics are diverse and extensive, this course is developed around a common thread connecting them all, such that each topic builds off the others.

Lectures will cover the relevant theory, and labs will familiarize the students with these topics from a practical point of view. Several of the lab assignments will be graded,
and a team project on reinforcement learning will form a major component of the grade - where the goal is to developing and deploy an agent in an environment and write a report analyzing the results.

Course Outline
--------------

A working outline can be found as topics below. This is subject to minor changes as the course progresses. 


Some recommended literature
---------------------------

TODO...


Lab sessions
------------

Jupyter Notebooks can either be executed on Google Colab (works nicely with Google Drive), MyBinder (don't forget to regularly save your work) or locally,
in which case Anaconda (2019.10 or above ; Python 3.7 or above) is strongly recommended.
If the conda command does not work, it's that conda is not in the PATH environment variable. You may add it with the command::

    export PATH="/usr/local/Anaconda3-2019.10/bin:$PATH"
    conda init

If you choose the "Local" version of the lab sessions, right click on the link > Save Link as...
If you wish to execute the notebooks on the machines of the Salle d'Informatique, download [this conda_environment.yml](conda_environment.yml) file open a terminal prompt and enter::

    conda env create -f conda_environment.yml
    python -m ipykernel install --user --name inf581 --display-name "Python (inf581)"

This will install all dependencies in a new conda environment named inf581. Once on the Notebook, don't forget to use Kernel > Change Kernel to use the Python (inf581) environment.
If the conda environment inf581 already exists, you may delete it with the following command::

    conda remove --name inf581 --all


To launch Jupyter, use::

    jupyter-notebook --ip=0.0.0.0 --port=8080


Dependencies
============

C.f. requirements.txt

.. _install:

Installation
============

Posix (Linux, MacOSX, WSL, ...)
-------------------------------

From the source code::

    conda deactivate         # Only if you use Anaconda...
    python3 -m venv env
    source env/bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements-jupyter.txt
    python3 setup.py develop


Windows
-------

From the source code::

    conda deactivate         # Only if you use Anaconda...
    python3 -m venv env
    env\Scripts\activate.bat
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements-jupyter.txt
    python3 setup.py develop


Lab sessions
============

Lab session 4: Dynamic Programming
----------------------------------

Subject:

- Open in Google Colab: https://colab.research.google.com/github/jeremiedecock/polytechnique-inf581-2021/blob/master/lab4_rl1_dynamic_programming.ipynb
- Open in MyBinder: https://mybinder.org/v2/gh/jeremiedecock/polytechnique-inf581-2021/master?filepath=lab4_rl1_dynamic_programming.ipynb
- Open in NbViewer: https://nbviewer.jupyter.org/github/jeremiedecock/polytechnique-inf581-2021/blob/master/lab4_rl1_dynamic_programming.ipynb
- Download the notebook file: https://github.com/jeremiedecock/polytechnique-inf581-2021/raw/master/lab4_rl1_dynamic_programming.ipynb

Solution:

- Open in Google Colab: https://colab.research.google.com/github/jeremiedecock/polytechnique-inf581-2021/blob/master/lab4_rl1_dynamic_programming_answers.ipynb
- Open in MyBinder: https://mybinder.org/v2/gh/jeremiedecock/polytechnique-inf581-2021/master?filepath=lab4_rl1_dynamic_programming_answers.ipynb
- Open in NbViewer: https://nbviewer.jupyter.org/github/jeremiedecock/polytechnique-inf581-2021/blob/master/lab4_rl1_dynamic_programming_answers.ipynb
- Download the notebook file: https://github.com/jeremiedecock/polytechnique-inf581-2021/raw/master/lab4_rl1_dynamic_programming_answers.ipynb


Lab session 6
-------------

Subject:

- Open in Google Colab: https://colab.research.google.com/github/jeremiedecock/polytechnique-inf581-2021/blob/master/lab6_rl2_tdlearning_qlearning_sarsa.ipynb
- Open in MyBinder: https://mybinder.org/v2/gh/jeremiedecock/polytechnique-inf581-2021/master?filepath=lab6_rl2_tdlearning_qlearning_sarsa.ipynb
- Open in NbViewer: https://nbviewer.jupyter.org/github/jeremiedecock/polytechnique-inf581-2021/blob/master/lab6_rl2_tdlearning_qlearning_sarsa.ipynb
- Download the notebook file: https://raw.githubusercontent.com/jeremiedecock/polytechnique-inf581-2021/master/lab6_rl2_tdlearning_qlearning_sarsa.ipynb

Solution:

- Open in Google Colab: https://colab.research.google.com/github/jeremiedecock/polytechnique-inf581-2021/blob/master/lab6_rl2_tdlearning_qlearning_sarsa_answers.ipynb
- Open in MyBinder: https://mybinder.org/v2/gh/jeremiedecock/polytechnique-inf581-2021/master?filepath=lab6_rl2_tdlearning_qlearning_sarsa_answers.ipynb
- Open in NbViewer: https://nbviewer.jupyter.org/github/jeremiedecock/polytechnique-inf581-2021/blob/master/lab6_rl2_tdlearning_qlearning_sarsa_answers.ipynb
- Download the notebook file: https://github.com/jeremiedecock/polytechnique-inf581-2021/raw/master/lab6_rl2_tdlearning_qlearning_sarsa_answers.ipynb

Lab session 7
-------------

Subject:

- Open in Google Colab: https://colab.research.google.com/github/jeremiedecock/polytechnique-inf581-2021/blob/master/lab7_rl3_reinforce.ipynb
- Open in MyBinder: https://mybinder.org/v2/gh/jeremiedecock/polytechnique-inf581-2021/master?filepath=lab7_rl3_reinforce.ipynb
- Open in NbViewer: https://nbviewer.jupyter.org/github/jeremiedecock/polytechnique-inf581-2021/blob/master/lab7_rl3_reinforce.ipynb
- Download the notebook file: https://github.com/jeremiedecock/polytechnique-inf581-2021/raw/master/lab7_rl3_reinforce.ipynb

Solution:

- Open in Google Colab: https://colab.research.google.com/github/jeremiedecock/polytechnique-inf581-2021/blob/master/lab7_rl3_reinforce_answers.ipynb
- Open in MyBinder: https://mybinder.org/v2/gh/jeremiedecock/polytechnique-inf581-2021/master?filepath=lab7_rl3_reinforce_answers.ipynb
- Open in NbViewer: https://nbviewer.jupyter.org/github/jeremiedecock/polytechnique-inf581-2021/blob/master/lab7_rl3_reinforce_answers.ipynb
- Download the notebook file: https://github.com/jeremiedecock/polytechnique-inf581-2021/raw/master/lab7_rl3_reinforce_answers.ipynb

Bonus:

- Open in Google Colab: https://colab.research.google.com/github/jeremiedecock/polytechnique-inf581-2021/blob/master/lab7_rl3_reinforce_baselines.ipynb
- Open in MyBinder: https://mybinder.org/v2/gh/jeremiedecock/polytechnique-inf581-2021/master?filepath=lab7_rl3_reinforce_baselines.ipynb
- Open in NbViewer: https://nbviewer.jupyter.org/github/jeremiedecock/polytechnique-inf581-2021/blob/master/lab7_rl3_reinforce_baselines.ipynb
- Download the notebook file: https://raw.githubusercontent.com/jeremiedecock/polytechnique-inf581-2021/master/lab7_rl3_reinforce_baselines.ipynb

Lab session 8
-------------

Subject:

- Open in Google Colab: https://colab.research.google.com/github/jeremiedecock/polytechnique-inf581-2021/blob/master/lab8_optim_cem.ipynb
- Open in MyBinder: https://mybinder.org/v2/gh/jeremiedecock/polytechnique-inf581-2021/master?filepath=lab8_optim_cem.ipynb
- Open in NbViewer: https://nbviewer.jupyter.org/github/jeremiedecock/polytechnique-inf581-2021/blob/master/lab8_optim_cem.ipynb
- Download the notebook file: https://github.com/jeremiedecock/polytechnique-inf581-2021/raw/master/lab8_optim_cem.ipynb

Solution:

- Open in Google Colab: https://colab.research.google.com/github/jeremiedecock/polytechnique-inf581-2021/blob/master/lab8_optim_cem_answers.ipynb
- Open in MyBinder: https://mybinder.org/v2/gh/jeremiedecock/polytechnique-inf581-2021/master?filepath=lab8_optim_cem_answers.ipynb
- Open in NbViewer: https://nbviewer.jupyter.org/github/jeremiedecock/polytechnique-inf581-2021/blob/master/lab8_optim_cem_answers.ipynb
- Download the notebook file: https://github.com/jeremiedecock/polytechnique-inf581-2021/raw/master/lab8_optim_cem_answers.ipynb
