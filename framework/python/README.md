# Python (2.7.x)
## ev3dev-lang-python
The Python example is based on the [Python language bindings for ev3dev](https://github.com/rhempel/ev3dev-lang-python) module for the ev3. 

## API Documentation
The online documentation can be found here: 

- Python language bidnings: http://python-ev3dev.readthedocs.io/en/latest/
- ev3dev language bindings: http://ev3dev-lang.readthedocs.io/en/latest/

## Setting Up the EV3 Brick
For Python 2.7.x the ev3dev-lang-python module is already 
installed on the ev3dev distribution.

## Development Environment
It's up to you how you want to develop. This section is just a suggestion how you could setting up your Python environment.

First download Python. We recommend the Anaconda Python distribution (https://www.continuum.io/downloads).

Create a new virtual environment with conda . http://conda.pydata.org/docs/using/envs.html

```bash
conda create -n ev3 python=2.7
```

Now you can switch to your Python environment.

```bash
source activate ev3
```

Next you need editor, you could use PyCharm Community version (https://www.jetbrains.com/pycharm/) or a simple editor like Brackets (http://brackets.io).

When you want autocomplection in PyCharm you can install the Python ev3 language bindings on your local machine.

```bash
cd framework/python
pip install -r requirements.txt
```

## Basic Robot Example
An example program that is written in Python and that uses the ev3dev-lang-python lib can be found here. 
- [robot.py](robot.py)
