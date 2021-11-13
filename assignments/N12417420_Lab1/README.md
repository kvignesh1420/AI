## Artificial Intelligence
### CSCI-GA.2560
#### [Lab 1](https://cs.nyu.edu/courses/fall21/CSCI-GA.2560-001/lab1.html)

### Algorithms:

- **Breadth First Search:** using a visited list to avoid duplicate vertices.

- **Iterative Deepening:** using the `-depth` parameter for initial depth, then increasing by 1. (Uses a visited list)

- **A\*:** using an `h` function of Euclidean distance from potential expansion node to goal.


### Python coding style

The assignment is written in python3 and alligns with the
[Google Python Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md)

The `.pylintrc` file has been referenced directly from the [Tensorflow project](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/tools/ci_build/pylintrc), with
a slight modification w.r.t `max-line-length`. To install `pylint` and check all files with `pylint` against TensorFlow's custom style definition:

```bash
pip3 install pylint
pylint --rcfile=./.pylintrc ./*.py
```

### Running the code

The code is written in `python3` can be executed using the `python>=3.6` interpreters.

#### Help with executions

```console
$ python3 path.py -h

usage: path.py [-h] [-v V] [-start START] [-goal GOAL] [-alg ALG] [-depth DEPTH] graph_file

Find a path from start node to a goal node

positional arguments:
  graph_file    Path to the graph input

optional arguments:
  -h, --help    show this help message and exit
  -v V          Enable verbosity for program runs
  -start START  Name of the start node
  -goal GOAL    Name of the goal node
  -alg ALG      One of: BFS, ID, ASTAR
  -depth DEPTH  Initial search depth (ONLY) for Iterative Deepening (ID)

Search until you find it!
```

#### Executing the programs

The search algorithms can be used as follows:

```console
# Run Breadth first search
$ python3 path.py -start S -goal G -alg BFS tests/input1.txt

# With verbosity
$ python3 path.py -v -start S -goal G -alg BFS tests/input1.txt

# Run Iterative deepening search
$ python3 path.py -start S -goal G -alg ID -depth 2 tests/input1.txt

# With verbosity
$ python3 path.py -v -start S -goal G -alg ID -depth 2 tests/input1.txt

# Run A-STAR search
$ python3 path.py -start S -goal G -alg ASTAR tests/input1.txt

# With verbosity
$ python3 path.py -v -start S -goal G -alg ASTAR tests/input1.txt
```

Here, `tests/input1.txt` is the path to the `graph_file`. **Please modify this path along with the input arguments for getting the search results.**
