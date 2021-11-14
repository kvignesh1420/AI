## Artificial Intelligence
### CSCI-GA.2560
#### [Lab 3](https://cs.nyu.edu/courses/fall21/CSCI-GA.2560-001/lab3.html)

### Algorithms:

- A Markov Process Solver using value and policy iterations.

### Python coding style

The assignment is written in python3 and aligns with the
[Google Python Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md)

The `.pylintrc` file has been referenced directly from the [Tensorflow project](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/tools/ci_build/pylintrc), with
a slight modification w.r.t `max-line-length`. To install `pylint` and check all files with `pylint` against TensorFlow's custom style definition:

```bash
pip3 install pylint
pylint --rcfile=./.pylintrc ./*.py
```

### Running the code

The code is written in `python3` can be executed using the `python>=3.6` interpreters.
**NOTE: The code depends on the [PLY](https://github.com/dabeaz/ply) and numpy python packages.**

The packages are present on the CIMS machines.

```console
$ pip3 list | grep ply
ply                                3.11
$ pip3 list | grep numpy
numpy                            1.19.5
```

However, they can be installed using:
```
$ pip3 install ply numpy
```
Please make sure that the `pip3` corresponds to the `python3` that we use for executing the programs.

#### Help with executions

```console
usage: mdp.py [-h] [-v] [-df DF] [-min MIN] [-tol TOL] [-iter ITER] input_file

Markov process solver

positional arguments:
  input_file  Path to the input file

optional arguments:
  -h, --help  show this help message and exit
  -v          Enable verbosity for program runs
  -df DF      future reward discount factor in the range [0, 1]. Defaults to 1.
  -min MIN    minimize values as costs, defaults to False which maximizes values as rewards
  -tol TOL    tolerance for each value iteration. Defaults to 0.01
  -iter ITER  Maximum number of value iteration updates before termination. Defaults to 100

Approximate the best approach!
```

#### Executing the programs

The program can be executed with different options as follows:

```console
# Run the solver with default options
$ python3 mdp.py ../tests/lab3_input1.txt

# Run the solver with default options in verbose mode
$ python3 mdp.py -v ../tests/lab3_input1.txt

# Run the solver with cost minimizer option
$ python3 mdp.py -min True ../tests/lab3_input3.txt

# Run the solver with a discount factor of 0.9
$ python3 mdp.py -df 0.9 ../tests/lab3_input6.txt
```

**NOTE: The `input_file` value given in the examples above are just for reference and have to be modified w.r.t proper test file paths**
