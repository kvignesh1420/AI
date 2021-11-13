## Artificial Intelligence
### CSCI-GA.2560
#### [Lab 2](https://cs.nyu.edu/courses/fall21/CSCI-GA.2560-001/lab2.html)

### Algorithms:
- A BNF to CNF converter using the 'cnf' mode
- A generic DPLL solver using the 'dpll' mode
- A direct BNF solver using the 'solver' mode.

#### Explanation:

The Bachus-Naur Form (BNF) to Conjunctive Normal Form (CNF) conversion is implemented by:
- Tokening the CNF sentences using lex followed by
- Building an parse tree using the yacc grammar rules, followed by
- applying the resolution algorithm recursively on the tree to achieve the CNF form.

**NOTE: After converting BNF clauses to CNF, a CNF clause is resolved if it contains a literal and it's negation.**

The output in CNF form or input from an external file is now used by the DPLL solver to solve
for a set of assignments to the atoms. If no valid solution/assignment exists, it returns:
"NO VALID ASSIGNMENT"

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
**NOTE: The code depends on the PLY python package for lax/yacc implementations**
The package is present on the CIMS machines.

```console
$ pip3 list | grep ply
ply                                3.11
```

However, it can be installed using:
```
$ pip3 install ply
```
Please make sure that the `pip3` corresponds to the `python3` that we use for executing the programs.

#### Help with executions
```console
$ python3 solver.py -h
usage: solver.py [-h] [-v] [-mode MODE] input_file

Propositional logic solver

positional arguments:
  input_file  Path to the input file

optional arguments:
  -h, --help  show this help message and exit
  -v          Enable verbosity for program runs
  -mode MODE  Mode to run the program. One of cnf, dpll, solver.

Solve it!
```

#### Executing the programs

The program can be executed in different modes as follows:

```console
# Run in 'cnf' mode:
$ python3 solver.py -mode cnf ../tests/lab2_input2.txt

# Run in 'cnf' mode with verbose output:
$ python3 solver.py -v -mode cnf ../tests/lab2_input2.txt

# Run in 'dpll' mode:
$ python3 solver.py -mode dpll ../tests/lab2_input3.txt

# Run in 'dpll' mode with verbose output:
$ python3 solver.py -v -mode dpll ../tests/lab2_input3.txt

# Run in 'solver' mode:
$ python3 solver.py -mode solver ../tests/lab2_input2.txt

# Run in 'solver' mode with verbose output:
$ python3 solver.py -v -mode solver ../tests/lab2_input2.txt
```

**NOTE: The `input_file` value given in the examples above are just for reference and have to be modified w.r.t proper test file paths**